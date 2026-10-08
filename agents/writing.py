from autogen_core.models import UserMessage

from agents.base import load_model


class WritingAgent:

    def __init__(self):
        self.model = load_model("writing")

    async def run(self, research_notes):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 연구 노트를 바탕으로 논리적이고 체계적인 Markdown 문서를 작성하라.

연구 노트:
{research_notes}

가상 값이나 합성된 값을 실제 관찰로 주장하지 마라.
""",
                    source="user"
                )
            ]
        )

        return result.content
