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

    async def evaluate_final(self, final_document):

        result = await self.model.create(
            messages=[
                UserMessage(
                    content=f"""
다음은 Revision이 생성한 최종 Markdown 문서다.

{final_document}

이 문서를 최종 저장하기 전에 엄격하게 평가하라.

평가 항목:
- 문서에 포함된 사용자 목표와의 일치
- 사실 오류
- 논리적 모순
- 근거 없는 주장
- 만들어낸 데이터 출처
- 만들어낸 데이터셋 이름, 경로 또는 열
- 가상 예제를 실제 분석으로 제시한 내용
- 실제 계산 없이 제시한 수치 결과
- 설명과 코드의 불일치
- 누락된 import
- 정의되지 않은 변수
- 코드 문법 오류 또는 실행 오류
- 생성 또는 병합 전에 참조된 열
- 실제 분석 변수의 결측값 처리
- 부적절한 통계 검정 선택
- 독립표본과 대응표본 설계의 구분
- Student와 Welch t-test의 구분
- Pearson과 Spearman 상관분석의 구분
- 효과크기와 신뢰구간 보고
- 상관관계를 인과관계로 해석한 내용
- 문서 전체를 감싼 불필요한 Markdown 코드 울타리

통계적 판정 규칙:
- scipy.stats.ttest_ind의 기본값은 equal_var=True다.
- Welch 독립표본 t-test는 equal_var=False를 명시해야 한다.
- 일반적인 R의 두 표본 t.test 기본값은 var.equal=False다.
- 등분산 위반만으로 Mann-Whitney U를 선택하면 안 된다.
- Mann-Whitney U를 자동으로 평균 차이 검정으로 해석하면 안 된다.
- Pearson 상관분석에서는 선형성과 영향력 있는 이상치를 검토해야 한다.
- 결측값은 실제 분석에 사용하는 변수를 기준으로 처리해야 한다.
- 비어 있는 비교 집단은 치명적 오류다.
- 실제 제공된 데이터로 계산하지 않은 통계값을 관측 결과로 제시하면 안 된다.

JSON만 반환하라.
Markdown 코드 울타리와 JSON 외 설명을 사용하지 마라.

정확히 다음 필드를 사용하라:

{{
  "status": "PASS or FAIL",
  "score": 0,
  "critical_errors": [],
  "required_revisions": []
}}

판정 규칙:
- score는 0부터 100까지의 정수여야 한다.
- critical_errors와 required_revisions는 문자열 목록이어야 한다.
- required_revisions는 구체적이고 직접 실행 가능한 수정 지침이어야 한다.
- score가 85 이상이어야 한다.
- critical_errors가 비어 있어야 한다.
- 문서가 포함된 사용자 목표와 일치해야 한다.
- 코드는 문서에 명시된 입력을 기준으로 내부적으로 실행 가능해야 한다.
- 조작되거나 계산되지 않은 관측 결과가 없어야 한다.

위 조건을 모두 만족할 때만 status를 PASS로 판정하라.
그 외에는 반드시 FAIL로 판정하라.
""",
                    source="user",
                )
            ],
            extra_create_args={
                "think": False,
            },
        )

        return result.content
