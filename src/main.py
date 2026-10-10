import asyncio
import json
from pathlib import Path

from workflows.dynamic_workflow import DynamicWorkflow


async def main():

    goal = """
올림픽 데이터셋을 분석하여
상관분석과 t-test 예제를 생성하는
Markdown 문서를 작성하라.
"""

    workflow = DynamicWorkflow()

    def save_debug_artifacts(context):
        debug_dir = Path("outputs/debug")
        debug_dir.mkdir(parents=True, exist_ok=True)

        (debug_dir / "goal.md").write_text(context.goal, encoding="utf-8")

        artifacts = {
            "research": context.artifacts.get("research", ""),
            "coding": context.artifacts.get("coding", ""),
            "writing": context.artifacts.get("writing", ""),
            "review": context.artifacts.get("review", ""),
            "revision": context.artifacts.get("revision", ""),
            "qa_review": context.artifacts.get("qa_review", ""),
            "qa_status": context.artifacts.get("qa_status", ""),
        }

        for name, content in artifacts.items():
            (debug_dir / f"{name}.md").write_text(str(content) if content else "", encoding="utf-8")

        metadata = {
            "created_at": context.created_at,
            "metadata": context.metadata,
        }

        (debug_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print("\n[SAVED] outputs/debug artifacts")

    try:
        result = await workflow.run(goal)
    finally:
        if workflow.last_context:
            save_debug_artifacts(workflow.last_context)

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
