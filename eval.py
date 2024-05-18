# Please clone the CLIcK repository(https://github.com/rladmstn1714/CLIcK/) to the same directory as this repository.

import glob
import json
import pandas as pd

result = pd.read_csv("results/gpt-4o-2024-05-13.csv")

file_dict = {
    "History": "../CLIcK/Dataset/Culture/Korean History",
    "Geography": "../CLIcK/Dataset/Culture/Korean Geography",
    "Law": "../CLIcK/Dataset/Culture/Korean Law",
    "Politics": "../CLIcK/Dataset/Culture/Korean Politics",
    "Society": "../CLIcK/Dataset/Culture/Korean Society",
    "Tradition": "../CLIcK/Dataset/Culture/Korean Tradition",
    "Economy": "../CLIcK/Dataset/Culture/Korean Economy",
    "Pop Culture": "../CLIcK/Dataset/Culture/Korean Popular",
    "Textual": "../CLIcK/Dataset/Language/Textual",
    "Functional": "../CLIcK/Dataset/Language/Functional",
    "Grammar": "../CLIcK/Dataset/Language/Grammar",
}

id_to_category = {}

for category, dir_path in file_dict.items():
    file_paths = glob.glob(f"{dir_path}/*.json")
    for file_path in file_paths:
        with open(file_path, "r") as f:
            data = json.loads(f.read())
            for x in data:
                id_to_category[x["id"]] = category

result["category"] = result["id"].map(id_to_category)
result["correct"] = result["answer"] == result["pred"]
print(result.groupby(["category"])["correct"].agg(["mean", "count"]))
