import json
import asyncio

from agents.planner import Planner
from agents.research import ResearchAgent
from agents.writing import WritingAgent
from agents.review import ReviewAgent
from agents.coding import CodingAgent


class DynamicWorkflow:

    def __init__(self):

        self.planner = Planner()

    async def run(self, goal):

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

        #
        # 1. Research
        #
        research_result = ""

        if "research" in tasks:

            print("\n[RUNNING] research")

            research_result = await ResearchAgent().run(goal)

        #
        # 2. Coding + Writing 병렬 실행
        #
        coding_result = ""
        writing_result = ""

        parallel_tasks = []

        if "coding" in tasks:

            print("[QUEUE] coding")

            parallel_tasks.append(
                CodingAgent().run(research_result)
            )

        if "writing" in tasks:

            print("[QUEUE] writing")

            parallel_tasks.append(
                WritingAgent().run(research_result)
            )

        if parallel_tasks:

            results = await asyncio.gather(
                *parallel_tasks
            )

            idx = 0

            if "coding" in tasks:
                coding_result = results[idx]
                idx += 1

            if "writing" in tasks:
                writing_result = results[idx]

        #
        # 3. 통합 결과 생성
        #
        combined_result = f"""
# Research Result

{research_result}

---

# Coding Result

{coding_result}

---

# Writing Result

{writing_result}
"""

        #
        # 4. Review
        #
        review_result = ""

        if "review" in tasks:

            print("\n[RUNNING] review")

            review_result = await ReviewAgent().run(
                combined_result
            )

        #
        # 5. 최종 결과
        #
        final_result = f"""
{combined_result}

---

# Review Result

{review_result}
"""

        return final_result
