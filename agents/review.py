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
{text}

검토 항목:
1. Factual Errors
2. Logical Contradictions
3. Statistical Errors
4. Unsupported Claims
5. Invented Data Sources, Dataset Names, or Columns
6. Code that Cannot Run with Documented Inputs
7. Missing Imports or Undefined Variables
8. Explanation and Code Inconsistencies
9. Hypothetical Examples Presented as Actual Analysis
10. Causal Claims Based Only on Correlation

통계적 검토:
- Pearson vs Spearman Selection
- Coefficient Ranges
- Independent vs Paired Observations
- Student vs Welch t-test
- Normality and Variance Assumptions
- Missing-Value Handling
- Group Comparability
- Effect-Size and Confidence-Interval Reporting

추가 규칙:
- Unequal variance가 반드시 Mann-Whitney U를 요구하지 않음.
- Equal variance가 확립되지 않은 경우 Welch t-test를 요구.
- 데이터셋 이름, 소스, 경로, 열은 User Goal에서 명시되지 않은 경우 가정으로 간주.
- Required Revisions는 구체적이고 실행 가능한 지침이어야 함.
- 원본 문서를 재작성하거나 칭찬하지 말 것.

결과를 다음 Markdown 섹션으로 반환하라:
# Critical Errors
# Goal Alignment Issues
# Statistical Issues
# Code Issues
# Unsupported Assumptions
# Required Revisions

300단어 이하로 답변하라.
""",
                    source="user",
                )
            ],
            extra_create_args={
                "think": False,
            },
        )

        return result.content
