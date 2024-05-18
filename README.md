# Evaluate GPT-4o on CLIcK

한국에 대한 문화적 지식과 언어적 지능을 평가하는 CLIcK 데이터셋에 대해 GPT-4o, GPT-4-turbo를 평가해보았습니다. 어떤 프롬프트를 사용하냐에 따라서도 성능 차이가 날 수 있기에 논문에서 사용한 프롬프트와 실험 방법을 그대로 사용하였습니다.

추가적인 분석을 하고 싶으실 수도 있을 것 같아서, 평가 코드와 평가를 위해 수집한 LLM 응답을 csv 파일로 저장해두었습니다.

👉 Learn more about **CLIcK** - [paper](https://arxiv.org/abs/2403.06412), [repository](https://github.com/rladmstn1714/CLIcK/blob/main/README.md), [huggingface](https://huggingface.co/datasets/EunsuKim/CLIcK)

## Results

> [!IMPORTANT]
> * 원 논문에서 SOTA 였던 GPT-3.5, Claude 2 모델과 GPT-4-turbo, GPT-4o를 비교해보았습니다. GPT-4-turbo만 하더라도 GPT-3.5, Claude 2를 크게 이겼는데, GPT-4o는 GPT-4-turbo도 이겼습니다.
> * 이렇게까지 차이가 날줄은 예상하지 못했는데요. GPT-4o가 가히 압도적으로 GPT-4-turbo를 모든 카테고리에서 이겼습니다. Average 값만 보아도 정말 큰 향상이 이뤄진 것을 알 수 있습니다.

**Conclusion: GPT-4o가 한국어, 한국 문화에 대해서도 성능이 많이 늘었다는 걸 체감해볼 수 있었습니다. GPT-4o를 쓰지 않을 이유가 없네요.**

### Korean Culture

|                | GPT-3.5 | Claude2 | GPT-4-turbo (New!) | **GPT-4o (New!)** |
|----------------|---------|---------|-------------|---------|
| History        | 31.32   | 35.00   | 43.93       | **65.12**   |
| Geography      | 45.42   | 43.30   | 80.66       | **81.42**  |
| Law            | 55.31   | 57.09   | 59.97       | **68.19**   |
| Politics       | 47.50   | 44.60   | 86.11       | **89.29**   |
| Society        | 50.20   | 49.33   | 86.08       | **91.26**   |
| Tradition      | 50.16   | 52.10   | 79.43       | **86.19**   |
| Economy        | 53.62   | 59.56   | 89.27       | **93.22**   |
| Pop culture    | 68.61   | 53.62   | 91.87       | **97.56**   |
| **Average**    | **49.30**   | **51.72**   | **71.75**  | **80.42**   |

### Korean Language

|                | GPT-3.5 | Claude2 | GPT-4-turbo (New!) | **GPT-4o (New!)** |
|----------------|---------|---------|-------------|---------|
| Textual        | 53.19   | 55.86   | 87.72       | **91.23**  |
| Functional     | 36.62   | 32.88   | 78.13       | **83.47**   |
| Grammar        | 36.62   | 47.42   | 44.17       | **56.94**   |
| **Average**    | **42.32**   | **45.39**   | **69.79**  | **77.08**   |

## Some Issues

### 1. Model Issue

`debug.log` 를 보다시피 우리 금쪽이(LLM)가 single word로 답하라 했지만 그렇게 내뱉지 않는 경우도 종종 있습니다. 기존 평가 방식과의 형평성을 위해 Prompt를 따로 수정하진 않았고, equal 조건이 아닌 답이 response에 포함되어 있는 경우에 정답으로 처리하도록 하였습니다.

```
id: KIIP_society_120 (2), answer: A, pred: A, response: A: 요금 할인
id: KIIP_society_111 (1), answer: D, pred: D, response: D: 신분증
```

### 2. Dataset Issue

데이터셋 상에 이슈가 있어서, 원본 레포에 이슈를 등록해둔 상태입니다. 이슈가 된 데이터 예시는 다음과 같습니다.

👉 https://github.com/rladmstn1714/CLIcK/issues/4

```
    {
        "id":"CSAT_geography_09_4",
        "paragraph":"",
        "question":"다음은 한국의 지리에 대한 문제이다.\n다음 글의 ᄀ~ᄅ에 대한 옳은 설명만을 <보기>에서 있는 대로 고른 것은? \n파랑의 작용이 활발한 해안에서는 기반암이 파식 작용을 받아 형성된 절벽인 ( ᄀ )와 넓고 평탄한 파식대가 나타난다. 파식대는 오랜 시간이 경과하면 파랑의 영향이 미치지 않는 고도에서 계단모양의 ( ᄂ )(으)로 변화되기도 한다. 파랑의 작용이 약한 곳에서는 하천이 운반한 모래와 해안의 돌출부에서 이동된 모래가 해안에 퇴적되어 ( ᄃ )이 형성될수있다.( ᄃ )의 모래가 사주를 이루어 만의 입구 를 막으면 ( ᄅ )이 형성된다. \n<보 기> \nᄀ. ᄀ의 후퇴 과정에서 시스택이 형성되기도 한다.\nᄂ. ᄂ은 지반 융기와 해수면 변동의 영향으로 형성된다.\nᄃ. ᄃ은 주로 양식장이나 염전으로 이용된다.\nᄅ. ᄅ의 대부분은 하천의 퇴적 작용이나 매립으로 규모가 작아지고 있다.",
        "choices":[
            "ᄀ, ᄂ",
            "ᄂ, ᄃ",
            "ᄃ, ᄅ",
            "ᄀ, ᄂ, ᄅ",
            "ᄀ, ᄃ, ᄅ "
        ],
        "answer":"ᄀ, ᄂ, ᄅ "
    },
```

공백 때문에 answer 값이 choices 내에 존재하지 않습니다. 이번 평가를 할 때는 모든 문자열에 대해 `.strip()` 적용하여 해결하였습니다.

그리고 id랑 category 매핑이 데이터셋에서는 되어있지 않아서, 공식 레포를 클론받아 데이터 구조를 보고 매핑을 해주었습니다. `eval.py` 참고해주세요.

## Quick Start

0. python 3.8 버전에서 실행되었으며, `requirements.txt` 에 명시된 라이브러리를 설치해주세요.

```bash
pip install -r requirements.txt
```

1. `.env` 파일을 만들어서 다음과 같이 환경 변수를 설정해주세요.

```ini
OPENAI_API_KEY=<YOUR_OPEN_API_KEY>
MODEL_VERSION=gpt-4o-2024-05-13
```

2. 다음 명령어를 실행하여 평가를 수행합니다. (이미 결과는 ./results 폴더에 저장되어 있습니다.)
   
```bash
python main.py
```

3. 결과를 계산하기 위해 `eval.py` 를 실행합니다.

```bash
❯ python eval.py
                 mean  count
category                    
Economy      0.932203    177
Functional   0.834667    375
Geography    0.814249    393
Grammar      0.569444    720
History      0.651190    840
Law          0.681887    657
Politics     0.892857    252
Pop Culture  0.975610    123
Society      0.912621    927
Textual      0.912281    855
Tradition    0.861862    666
```

### Acknowledgement

Thanks to [Corca](https://www.corca.team/) team for providing the API to do this project. 🙏

### References

```bibtex
@misc{kim2024click,
      title={CLIcK: A Benchmark Dataset of Cultural and Linguistic Intelligence in Korean}, 
      author={Eunsu Kim and Juyoung Suk and Philhoon Oh and Haneul Yoo and James Thorne and Alice Oh},
      year={2024},
      eprint={2403.06412},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```