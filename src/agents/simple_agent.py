from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt

# from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from rich import print  # pylint: disable=redefined-builtin

from src import base_model
from src.front_end import interactive_console
from src.guardrails import check_abusive_service
from src.prompts import (
    angry_mood_system_prompt,
    angry_mood_system_prompt_agent_fault,
    base_neutral_promnpt,
    happy_mood_system_prompt,
    sad_mood_system_prompt,
    sad_mood_system_prompt_agent_fault,
)
from src.states.mood import MoodMiddleware
from src.tools import get_air_quality, get_geolocation_by_city, get_weather


@dynamic_prompt
def user_moode_based_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user mood."""

    user_mood = request.state.get("user_mood")
    base_prompt = base_neutral_promnpt
    print("The mood is:", user_mood)
    if user_mood["user_mood"] == "happy":
        return happy_mood_system_prompt
    if (user_mood["user_mood"] == "sad") and (user_mood["reason"] == "agent"):
        return sad_mood_system_prompt_agent_fault
    if (user_mood["user_mood"] == "sad") and (user_mood["reason"] == "other"):
        return sad_mood_system_prompt
    if (user_mood["user_mood"] == "angry") and (user_mood["reason"] == "agent"):
        return angry_mood_system_prompt_agent_fault
    if (user_mood["user_mood"] == "angry") and (user_mood["reason"] == "other"):
        return angry_mood_system_prompt
    return base_prompt


simple_agent = create_agent(
    model=base_model,
    checkpointer=InMemorySaver(),
    middleware=[check_abusive_service, MoodMiddleware(), user_moode_based_prompt],
    tools=[get_air_quality, get_weather, get_geolocation_by_city],
)


if __name__ == "__main__":
    interactive_console(simple_agent)
    # messages = {
    #     "messages": [
    #         HumanMessage(content="Hello :) I am in good mood tell me a joke"),
    #     ],
    #     "user_mood": {"mood": "neutral", "reason": "other"},
    # }
    # response = simple_agent.invoke(messages)
    # print(response)
    # for stream_mode, chunk in simple_agent.stream(messages, stream_mode=["updates", "custom"]):
    #     print(f"stream_mode: {stream_mode}")
    #     print(f"content: {chunk}")
    #     print("\n")
