import json
import asyncio

from agents.planner import Planner
from agents.research import ResearchAgent
from agents.writing import WritingAgent
from agents.review import ReviewAgent
from agents.coding import CodingAgent

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

        tasks = plan["agents"]

        if "review" not in tasks:
            tasks.append("review")

        print("\n[SELECTED AGENTS]")
        print(tasks)

        context.metadata["selected_agents"] = tasks

        #
        # RESEARCH
        #

        if "research" in tasks:

            print("\n[RUNNING] research")

            context.research = await (
                ResearchAgent().run(
                    context.goal
                )
            )

        #
        # PARALLEL WORK
        #

        parallel_tasks = []

        if "coding" in tasks:

            print("[QUEUE] coding")

            parallel_tasks.append(
                CodingAgent().run(
                    context.research
                )
            )

        if "writing" in tasks:

            print("[QUEUE] writing")

            parallel_tasks.append(
                WritingAgent().run(
                    context.research
                )
            )

        if parallel_tasks:

            results = await asyncio.gather(
                *parallel_tasks
            )

            idx = 0

            if "coding" in tasks:

                context.coding = results[idx]

                idx += 1

            if "writing" in tasks:

                context.writing = results[idx]

        #
        # COMBINED RESULT
        #

        combined_result = f"""
# Research Result

{context.research}

---

# Coding Result

{context.coding}

---

# Writing Result

{context.writing}
"""

        #
        # REVIEW
        #

        if "review" in tasks:

            print("\n[RUNNING] review")

            context.review = await (
                ReviewAgent().run(
                    combined_result
                )
            )

        #
        # FINAL OUTPUT
        #

        final_result = f"""
# Charles AI Result

## Goal

{context.goal}

---

# Research Result

{context.research}

---

# Coding Result

{context.coding}

---

# Writing Result

{context.writing}

---

# Review Result

{context.review}
"""

        return final_result
