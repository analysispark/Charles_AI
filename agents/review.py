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
1. 사실 오류
2. 논리 오류
3. 통계적 오류
4. 실행 불가능한 코드
5. 지원되지 않는 또는 조작된 주장
6. 구체적인 수정 지침

{text}

300단어 이하로 답변하라.
""",
                    source="user"
                )
            ]
        )

        return result.content
