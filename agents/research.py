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

구조화된 연구 노트를 작성하라. 다음 섹션을 포함하라:
- 핵심 개념
- 필요한 증거
- 방법론
- 가정
- 제한 사항
- 확인이 필요한 사실

최종 보고서는 작성하지 않아도 된다.
""",
                    source="user"
                )
            ]
        )

        return result.content
