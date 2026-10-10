import json
import asyncio

from agents.planner import Planner
from agents.research import ResearchAgent
from agents.writing import WritingAgent
from agents.review import ReviewAgent
from agents.coding import CodingAgent
from agents.revision import RevisionAgent

from src.context import TaskContext


class DynamicWorkflow:

    def __init__(self):

        self.planner = Planner()

    async def run(self, goal):

        context = TaskContext()

        context.goal = goal

        print("\n[PLANNER]")

        plan_text = await self.planner.create_plan(goal)

        print(plan_text)

        try:
            if isinstance(plan_text, dict):
                plan = plan_text
            else:
                start = plan_text.find("{")
                end = plan_text.rfind("}") + 1

                json_text = plan_text[start:end]

                plan = json.loads(json_text)
        except Exception as e:

            print("\n[WARNING]")
            print("Planner JSON 파싱 실패")
            print(e)

            plan = {
                "agents": [
                    "research",
                    "writing",
                    "review"
                ]
            }

        if not isinstance(plan, dict) or "agents" not in plan or not isinstance(plan["agents"], list):
            plan = {
                "agents": [
                    "research",
                    "writing",
                    "review"
                ]
            }

        tasks = [task for task in plan.get("agents", []) if isinstance(task, str) and task in ["research", "coding", "writing", "review", "revision"]]
        tasks = list(dict.fromkeys(tasks))


        # Ensure research, review, and revision are always included
        if "research" not in tasks:
            tasks.append("research")
        if "review" not in tasks:
            tasks.append("review")
        if "revision" not in tasks:
            tasks.append("revision")

        canonical_order = ["research", "coding", "writing", "review", "revision"]
        tasks = [task for task in canonical_order if task in tasks]

        print("\n[SELECTED AGENTS]")
        print(tasks)

        context.metadata["selected_agents"] = tasks

        #
        # RESEARCH
        #


        print("\n[RUNNING] research")

        context.artifacts["research"] = await (
            ResearchAgent().run(
                context.goal
            )
        )

        if not context.artifacts["research"].strip():
            raise RuntimeError("ResearchAgent returned an empty result")

        #
        # PARALLEL WORK
        #

        parallel_tasks = []

        shared_source_input = f"""
User Goal:
{context.goal}

Research Notes:
{context.artifacts["research"]}
"""

        if "coding" in tasks:

            print("[QUEUE] coding")

            parallel_tasks.append(
                CodingAgent().run(
                    shared_source_input
                )
            )

        if "writing" in tasks:

            print("[QUEUE] writing")

            parallel_tasks.append(
                WritingAgent().run(
                    shared_source_input
                )
            )

        if parallel_tasks:

            results = await asyncio.gather(
                *parallel_tasks
            )

            idx = 0

            if "coding" in tasks:

                context.artifacts["coding"] = results[idx]

                idx += 1

            if "writing" in tasks:

                context.artifacts["writing"] = results[idx]

        #
        # REVIEW
        #


        print("\n[RUNNING] review")

        review_input = f"""
User Goal:
{context.goal}

Writing Result:
{context.artifacts["writing"]}

Coding Result:
{context.artifacts["coding"]}
"""

        context.artifacts["review"] = await (
            ReviewAgent().run(
                review_input
            )
        )

        #
        # REVISION
        #


        print("\n[RUNNING] revision")

        context.artifacts["revision"] = await (
            RevisionAgent().run(
                writing_result=f"""
User Goal:
{context.goal}

Writing Result:
{context.artifacts["writing"]}
""",
                coding_result=context.artifacts["coding"],
                review_result=context.artifacts["review"]
            )
        )

        #
        # FINAL OUTPUT
        #

        return context.artifacts["revision"]
