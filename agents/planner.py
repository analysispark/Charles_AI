# class Planner:
#
#     def create_plan(self, goal):
#
#         plan = []
#
#         goal_lower = goal.lower()
#
#         plan.append("research")
#
#         if (
#             "python" in goal_lower
#             or "코드" in goal
#             or "프로그램" in goal
#         ):
#             plan.append("coding")
#
#         plan.append("writing")
#         plan.append("review")
#
#         return plan

import json

from autogen_core.models import UserMessage

from agents.base import load_model


class Planner:

    def __init__(self):

        self.model = load_model("planner")

    async def create_plan(self, goal):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
너는 AI 프로젝트 관리자다.

사용 가능한 Agent는 아래와 같다.

research
- 조사
- 배경지식 수집
- 자료 분석

coding
- Python
- Shell
- Bash
- R
- 프로그래밍

writing
- Markdown 작성
- 문서 작성
- 위키 작성
- 보고서 작성

review
- 논리 검토
- 오류 검토
- 품질 검토

규칙:

1. 반드시 JSON만 출력한다.
2. 설명을 작성하지 않는다.
3. markdown을 사용하지 않는다.
4. 아래 형식을 따른다.

예시:

{{"agents":["research","writing","review"]}}

사용자 목표:

{goal}
""",
                    source="user"
                )
            ],
            extra_create_args={
                "think": False,
            }
        )

        return result.content
