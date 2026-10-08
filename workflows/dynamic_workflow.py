import json

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

        print("\n[SELECTED AGENTS]")
        print(tasks)

        result = goal

        for task in tasks:

            print(f"\n[RUNNING] {task}")

            if task == "research":

                result = await ResearchAgent().run(result)

            elif task == "writing":

                result = await WritingAgent().run(result)

            elif task == "coding":

                result = await CodingAgent().run(result)

            elif task == "review":

                review_result = await ReviewAgent().run(result)

                result = f"""
# Generated Content

{result}

---

# Review

{review_result}
"""

        return result
