import asyncio

from workflows.dynamic_workflow import DynamicWorkflow


async def main():

    goal = """
올림픽 데이터셋을 분석하여
상관분석과 t-test 예제를 생성하는
Markdown 문서를 작성하라.
"""

    workflow = DynamicWorkflow()

    result = await workflow.run(goal)

    print("\n[FINAL RESULT]")
    print(result)

    with open(
        "outputs/result.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(result)

    print(
        "\n[SAVED] outputs/result.md"
    )


if __name__ == "__main__":

    asyncio.run(main())
