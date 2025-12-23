from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from rich import print


class GetWeather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


class GetPopulation(BaseModel):
    """Get the current population in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


if __name__ == "__main__":
    model = init_chat_model(
        temperature=0,
        credentials_profile_name="sandbox",
        region_name="eu-west-2",
        model_provider="bedrock_converse",
        configurable_fields=("model", "temperature", "max_tokens"),
    )
    model_with_tools = model.bind_tools([GetWeather, GetPopulation])

    response = model_with_tools.invoke(
        "what's bigger in 2024 LA or NYC",
        config={"configurable": {"model": "amazon.nova-micro-v1:0"}},
    )
    print(response)
    response = model_with_tools.invoke(
        "what's bigger in 2024 LA or NYC",
        config={"configurable": {"model": "amazon.nova-pro-v1:0"}},
    )
    print(response)
