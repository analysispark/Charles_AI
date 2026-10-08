from autogen_core.models import UserMessage

from agents.base import load_model


class ResearchAgent:

    def __init__(self):
        self.model = load_model("research")

    async def run(self, task):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 주제에 대해 조사해라.

{task}
""",
                    source="user"
                )
            ]
        )

        return result.content
