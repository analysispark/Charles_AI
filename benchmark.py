import time

from ollama import chat


MODELS = [
    "qwen3:8b",
    "qwen3.5:9b",
    "qwen2.5-coder:14b",
    "qwen3.6:27b-q4_K_M",
]


PROMPT = """
피어슨 상관분석의 개념과 수식을
500자 내외로 설명하라.
"""


for model in MODELS:

    print("=" * 60)
    print(model)

    start = time.time()

    response = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": PROMPT,
            }
        ],
    )

    elapsed = time.time() - start

    content = response["message"]["content"]

    chars = len(content)

    print(f"time   : {elapsed:.2f} sec")
    print(f"chars  : {chars}")
    print(f"char/s : {chars/elapsed:.1f}")

    print()
