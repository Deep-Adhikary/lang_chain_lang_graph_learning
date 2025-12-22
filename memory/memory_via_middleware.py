from typing import Any

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.tools import tool, ToolRuntime
from rich import print


class CustomState(AgentState):
    user_preferences: dict[str, Any]


@tool
def sample_tool(param: str, runtime: ToolRuntime[None, CustomState]) -> str:
    """A custom sample tool that accesses state."""
    print("User preferences from state in tool:", runtime.state.get("user_preferences"))
    print("Param:", param)
    return f"Sample tool received: {param}"


class CustomStateMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState
    tools = [sample_tool]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        # print("DEBUG LINE", state.user_preferences)
        return {"user_preferences": state["user_preferences"]}
