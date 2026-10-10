from agents.base import load_model
from autogen_core.models import UserMessage


class RevisionAgent:

    def __init__(self):
        self.model = load_model("revision")

    async def run(
        self,
        writing_result,
        coding_result,
        review_result,
    ):
        prompt = (
            f"{writing_result}\n\n"
            f"# Coding Result\n"
            f"{coding_result}\n\n"
            f"# Review Result\n"
            f"{review_result}\n\n"
            "Revision Instructions:\n"
            "- Treat the User Goal embedded in writing_result as authoritative.\n"
            "- Use Writing Result as the primary draft.\n"
            "- Incorporate Coding Result only if relevant, consistent, and executable.\n"
            "- Apply all valid instructions from Required Revisions.\n"
            "- If no actual dataset was supplied, describe the output as an analysis protocol or illustrative example.\n"
            "- Do not claim that IOC, Kaggle, or another source was actually used.\n"
            "- Do not claim that an actual analysis was performed.\n"
            "- Do not report invented statistics as observed results.\n"
            "- Label assumed dataset names, paths, and columns explicitly.\n"
            "- Do not reference a column before it is created or merged.\n"
            "- Do not use GDP or another external variable unless its source and merge step are explicitly documented.\n"
            "- Ensure included code has all imports, defined variables, and handles missing values.\n"
            "- Use na=False where appropriate for string matching when missing values may be present.\n"
            "- Clearly distinguish independent-samples and paired-samples designs, and use a statistical test appropriate to the actual design.\n"
            "- Use Welch t-test when equal variance is not established.\n"
            "- Remove contradictions between prose and code.\n"
            "- Return only the final revised Markdown document.\n"
            "- Do not include review or revision-process commentary."
        )

        response = await self.model.create(
            messages=[
                UserMessage(
                    content=prompt,
                    source="user",
                )
            ],
            extra_create_args={
                "think": False,
            },
        )

        return response.content
