from autogen_core.models import UserMessage

from agents.base import load_model


class ReviewAgent:

    def __init__(self):
        self.model = load_model("review")

    async def run(self, text):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 결과물을 검토하라.

검토 항목:

1. 논리 오류
2. 사실 오류
3. 개선 사항

300단어 이하로 답변하라.

{text}
""",
                    source="user"
                )
            ]
        )

        return result.content
