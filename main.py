import os
import multiprocessing as mp
from typing import Tuple

import openai
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from datasets import load_dataset

from prompts import TYPE_1, TYPE_2, TYPE_3, TYPE_4
from logger import logger


def get_prompt(x) -> str:
    num_choices = len(x["choices"])
    if num_choices == 4:
        if x["paragraph"] != "":  # Use Type 1 Prompt
            return TYPE_1.format(
                CONTEXT=x["paragraph"],
                QUESTION=x["question"],
                A=x["choices"][0],
                B=x["choices"][1],
                C=x["choices"][2],
                D=x["choices"][3],
            )
        else:
            return TYPE_2.format(
                QUESTION=x["question"],
                A=x["choices"][0],
                B=x["choices"][1],
                C=x["choices"][2],
                D=x["choices"][3],
            )
    elif num_choices == 5:
        if x["paragraph"] != "":
            return TYPE_3.format(
                CONTEXT=x["paragraph"],
                QUESTION=x["question"],
                A=x["choices"][0],
                B=x["choices"][1],
                C=x["choices"][2],
                D=x["choices"][3],
                E=x["choices"][4],
            )
        else:
            return TYPE_4.format(
                QUESTION=x["question"],
                A=x["choices"][0],
                B=x["choices"][1],
                C=x["choices"][2],
                D=x["choices"][3],
                E=x["choices"][4],
            )
    else:
        raise ValueError(f"Invalid number of choices: {num_choices} (ID: {x['id']})")


def get_answer(x) -> str:
    # 왜 이렇게 .strip() 처리를 해주었는지는 README에 issue 파트 참고 부탁드립니다.
    answer_idx = [xx.strip() for xx in x["choices"]].index(x["answer"].strip())
    if answer_idx == -1:
        raise ValueError(f"Answer not found in choices: {x['answer']} (ID: {x['id']})")
    return chr(0x41 + answer_idx)  # answer_idx = 0 -> answer = "A"


def get_pred(x) -> Tuple[str, str]:
    response = (
        client.chat.completions.create(
            model=MODEL_VERSION,
            messages=[{"role": "user", "content": get_prompt(x)}],
            temperature=0.0,
        )
        .choices[0]
        .message.content.strip()
        .replace('"', "")  # Remove double quotes
        .replace("'", "")  # Remove single quotes
    )

    if response.startswith("A"):
        pred = "A"
    elif response.startswith("B"):
        pred = "B"
    elif response.startswith("C"):
        pred = "C"
    elif response.startswith("D"):
        pred = "D"
    elif response.startswith("E"):
        pred = "E"
    else:
        pred = ""  # Wrong answer

    return pred, response


if __name__ == "__main__":
    MODEL_VERSION = "gpt-4-turbo-2024-04-09"

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        max_retries=3,
        timeout=60,
    )

    click_ds = load_dataset("EunsuKim/CLIcK")

    result = []
    for x in tqdm(click_ds["train"]):
        try:
            content = get_prompt(x)
            answer = get_answer(x)

            for trial in range(3):
                pred, response = get_pred(x)
                logger.debug(
                    f"id: {x['id']} ({trial}), answer: {answer}, pred: {pred}, response: {response}"
                )
                result.append([x["id"], trial, answer, pred, response])
        except ValueError as e:
            logger.error(e)
            continue

    df = pd.DataFrame(result, columns=["id", "trial", "answer", "pred", "response"])

    os.makedirs("results", exist_ok=True)
    df.to_csv(f"results/{MODEL_VERSION}.csv", index=False)
