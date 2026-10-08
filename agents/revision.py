from agents.base import load_model
from autogen_core.models import UserMessage

class RevisionAgent:
    def __init__(self):
        self.model = load_model("revision")

    async def run(self, writing_result, coding_result, review_result):
        prompt = (
            f"Create the final improved Markdown document based on the following inputs:\n"
            f"Writing Result: {writing_result}\n"
            f"Coding Result: {coding_result}\n"
            f"Review Result: {review_result}\n\n"
            "Instructions:\n"
            "- Preserve useful and supported content from Writing Result.\n"
            "- Incorporate valid executable code from Coding Result when present.\n"
            "- Apply valid revision instructions from Review Result.\n"
            "- Correct factual, logical, statistical, and code errors.\n"
            "- Remove unsupported or fabricated claims.\n"
            "- Clearly label synthetic or hypothetical examples.\n"
            "- Return only the final revised Markdown document.\n"
            "- Do not describe the revision process."
        )
        response = await self.model.create(
            messages=[
                UserMessage(
                    content=prompt,
                    source="user",
                )
            ]
        )
        return response.content
