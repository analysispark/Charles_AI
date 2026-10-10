import argparse
import asyncio
import json
from pathlib import Path

from workflows.dynamic_workflow import DynamicWorkflow


def parse_args():
    parser = argparse.ArgumentParser(description="Run the DynamicWorkflow with a specified goal.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("goal", nargs="?", help="The goal as a string.")
    group.add_argument("--goal-file", type=Path, help="Path to a file containing the goal.")
    parser.add_argument("--output", type=Path, default=Path("outputs/result.md"), help="Path to save the final result.")
    parser.add_argument("--debug-dir", type=Path, default=Path("outputs/debug"), help="Directory to save debug artifacts.")
    return parser.parse_args()


def load_goal(args):
    if args.goal:
        goal = args.goal.strip()
        if not goal:
            raise ValueError("The provided goal is empty or contains only whitespace.")
        return goal
    elif args.goal_file:
        if not args.goal_file.exists():
            raise FileNotFoundError(f"The goal file '{args.goal_file}' does not exist.")
        goal = args.goal_file.read_text(encoding="utf-8").strip()
        if not goal:
            raise ValueError("The goal file is empty or contains only whitespace.")
        return goal
    else:
        raise ValueError("No goal provided.")


def save_debug_artifacts(context, debug_dir):
    debug_dir = Path(debug_dir)
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

    print(f"\n[SAVED] {debug_dir} artifacts")


async def main():
    args = parse_args()
    goal = load_goal(args)

    workflow = DynamicWorkflow()


    try:
        result = await workflow.run(goal)
    finally:
        if workflow.last_context:
            save_debug_artifacts(workflow.last_context, args.debug_dir)

    print("\n[FINAL RESULT]")
    print(result)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        args.output,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(result)

    print(f"\n[SAVED] {args.output}")


if __name__ == "__main__":

    asyncio.run(main())
