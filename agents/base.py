import yaml

from autogen_ext.models.ollama import OllamaChatCompletionClient


def load_model(role):

    with open(
        "config/models.yaml",
        "r",
        encoding="utf-8"
    ) as f:

        config = yaml.safe_load(f)

    model_name = config[role]["model"]

    return OllamaChatCompletionClient(
        model=model_name,
        host="http://localhost:11434",
        option={
            "num_predict": 300,
        }
    )
