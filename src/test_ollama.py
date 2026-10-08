import asyncio

from autogen_core.models import UserMessage

from agents.base import load_model


async def main():

    model = load_model("research")

    result = await model.create(
        messages=[
            UserMessage(
                content="피어슨 상관분석을 3문장으로 설명해줘.",
                source="user",
            )
        ]
    )

    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
