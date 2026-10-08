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
1. Factual Errors
2. Logical Errors
3. Statistical Errors
4. Non-executable Code
5. Unsupported Claims
6. Concrete Revision Instructions

{text}

300단어 이하로 답변하라.
""",
                    source="user"
                )
            ]
        )

        return result.content
