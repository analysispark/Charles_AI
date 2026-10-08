from autogen_core.models import UserMessage
from agents.base import load_model


class RevisionAgent:

    def __init__(self):
        self.model = load_model("revision")

    async def run(self, writing_result, review_result):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음 결과물을 바탕으로 최종 문서를 개정하라.

Writing Result:
{writing_result}

Review Result:
{review_result}
""",
                    source="user"
                )
            ]
        )

        return result.content
