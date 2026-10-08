from autogen_core.models import UserMessage

from agents.base import load_model


class WritingAgent:

    def __init__(self):
        self.model = load_model("writing")

    async def run(self, text):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 내용을 Markdown 문서 형태로 작성하라.

{text}
""",
                    source="user"
                )
            ]
        )

        return result.content
