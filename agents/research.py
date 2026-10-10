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
- Core Concepts
- Required Evidence
- Methods
- Assumptions
- Limitations
- Facts Requiring Verification

최종 보고서는 작성하지 않아도 된다.
""",
                    source="user"
                )
            ],
            extra_create_args={
                "think": False,
            }
        )

        return result.content
