from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    wrap_model_call,
    wrap_tool_call,
)
from langchain.agents.structured_output import ToolStrategy
from langchain.messages import HumanMessage, SystemMessage, ToolMessage

from memory.memory_via_middleware import CustomStateMiddleware
from models import nova_micro, nova_pro
from tools.dog_info import DogInfo, get_dog_info


@wrap_tool_call
def handel_tool_errors(request: ModelRequest, handler: callable) -> ModelResponse:
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"An error occurred while using the tool: {str(e)}",
            tool_call_id=request.tool_call["id"],
        )


@wrap_model_call
def dynamic_model_selection_by_meesage_length(
    request: ModelRequest, handler
) -> ModelResponse:
    messate_count = len(request.state["messages"])
    if messate_count > 10:
        model = nova_pro
    else:
        model = nova_micro

    return handler(request.override(model=model))


def get_system_prompt() -> SystemMessage:
    return SystemMessage(
        content=[
            {
                "type": "text",
                "text": "You are a helpful assistant to answer questions about dogs.",
            },
            {
                "type": "text",
                "text": "You have access to a dog_info tool to get different information about dogs. You will pass dog breed names to the tool and get information about them.",
            },
            {
                "type": "text",
                "text": "Always provide response in DogInfo format.",
            },
        ]
    )


def create_human_message(query: str | list[str]) -> HumanMessage:
    return {
        "messages": [HumanMessage(content=query)],
        "user_preferences": {"style": "bullets", "verbosity": "detailed"},
    }


if __name__ == "__main__":
    agent = create_agent(
        model=nova_micro,
        system_prompt=get_system_prompt(),
        middleware=[
            dynamic_model_selection_by_meesage_length,
            handel_tool_errors,
            CustomStateMiddleware(),
        ],
        tools=[get_dog_info],
        response_format=ToolStrategy(DogInfo),
    )
    query = create_human_message("Tell me about Afghan Hound.")
    # print(query)
    # response = agent.invoke(query)
    # print(response)
    # print("\nStructured Response:\n")
    # print(response.get("structured_response", "No structured response found"))

    for chunk in agent.stream(query, stream_mode="values"):
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            print("====================Content====================")
            print(f"Agent: {latest_message.content}")
        elif latest_message.tool_calls:
            print("====================Tool Calls====================")
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
