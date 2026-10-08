import json
import asyncio

from agents.planner import Planner
from agents.research import ResearchAgent
from agents.writing import WritingAgent
from agents.review import ReviewAgent
from agents.coding import CodingAgent
from agents.revision import RevisionAgent  # 추가된 에이전트

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

            context.artifacts["research"] = await (
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
                    context.artifacts.get("research", "")
                )
            )

        if "writing" in tasks:

            print("[QUEUE] writing")

            parallel_tasks.append(
                WritingAgent().run(
                    context.artifacts.get("research", "")
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
        # COMBINED RESULT
        #

        combined_result = f"""
# Research Result

{context.artifacts.get("research", "")}

---

# Coding Result

{context.artifacts.get("coding", "")}

---

# Writing Result

{context.artifacts.get("writing", "")}
"""

        #
        # REVIEW
        #

        if "review" in tasks:

            print("\n[RUNNING] review")

            context.artifacts["review"] = await (
                ReviewAgent().run(
                    combined_result
                )
            )

        #
        # REVISION
        #

        if "revision" not in tasks:
            tasks.append("revision")

        if "revision" in tasks:

            print("\n[RUNNING] revision")

            context.artifacts["revision"] = await (
                RevisionAgent().run(
                    writing_result=context.artifacts.get("writing", ""),
                    review_result=context.artifacts.get("review", "")
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

{context.artifacts.get("research", "")}

---

# Coding Result

{context.artifacts.get("coding", "")}

---

# Writing Result

{context.artifacts.get("writing", "")}

---

# Review Result

{context.artifacts.get("review", "")}

---

# Revision Result

{context.artifacts.get("revision", "")}
"""

        return final_result
