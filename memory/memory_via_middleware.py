from typing import Any

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware

from tools.dog_info import get_dog_info


class CustomState(AgentState):
    user_preferences: dict[str, Any]


class CustomStateMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [get_dog_info]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None: ...
