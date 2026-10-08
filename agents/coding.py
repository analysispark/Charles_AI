from autogen_core.models import UserMessage

from agents.base import load_model


class CodingAgent:

    def __init__(self):

        self.model = load_model("coding")

    async def run(self, text):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 요구사항에 대한 코드를 작성하라.

요구사항:

{text}

규칙:

1. 실행 가능한 코드를 작성하라.
2. 코드에 주석을 포함하라.
3. 필요한 라이브러리를 명시하라.
4. 설명보다 코드를 우선 작성하라.
""",
                    source="user"
                )
            ]
        )

        return result.content

