import yaml

from autogen_ext.models.ollama import (
    OllamaChatCompletionClient
)


def load_model(role):

    with open(
        "config/models.yaml",
        "r",
        encoding="utf-8"
    ) as f:

        config = yaml.safe_load(f)

    model_name = config[role]["model"]

    #
    # AutoGen이 모르는 모델
    #
    if (
        "qwen3.5" in model_name
        or "qwen3.6" in model_name
        or "coder" in model_name
    ):

        return OllamaChatCompletionClient(
            model=model_name,
            model_info={
                "vision": False,
                "function_calling": False,
                "json_output": True,
                "family": "qwen",
            },
        )

    #
    # AutoGen 기본 지원 모델
    #
    return OllamaChatCompletionClient(
        model=model_name
    )
