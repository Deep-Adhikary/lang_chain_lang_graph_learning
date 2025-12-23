from dataclasses import asdict

from langchain.chat_models import init_chat_model
from rich import print  #pylint: disable=redefined-builtin

from src.configs import AWSConfig, nova_micro_config

base_model = init_chat_model(
    **asdict(AWSConfig()),
    **asdict(nova_micro_config),
    configurable_fields=("model", "temperature", "max_tokens"),
)

if __name__ == "__main__":
    response = base_model.invoke(
        "Hello from the configurable model!",
    )
    print(response)
