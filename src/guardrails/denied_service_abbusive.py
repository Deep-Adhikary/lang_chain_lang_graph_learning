from dataclasses import asdict
from typing import Any, Literal

from langchain.agents.middleware import AgentState, before_agent
from langchain.chat_models import init_chat_model
from langgraph.runtime import Runtime
from pydantic import BaseModel
from rich import print  # pylint: disable=redefined-builtin

from src.configs import AWSConfig, OllamaConfig, nova_lite_config, qwen_3_config
from src.prompts import abusive_checker_prompt


class AbusiveResponse(BaseModel):
    """Class to represent data if the user is abusive."""

    abusive: bool
    inappropriate_sexual_request: bool
    category: Literal[
        "hate",
        "profanity",
        "threats",
        "harassment",
        "sexual_harassment",
        "sexual_explicit",
        "personal_attack",
        "other",
    ]
    target: Literal["agent", "person", "group", "self", "unknown"]
    confidence: float
    rationale: str


abusive_detector = init_chat_model(
    **asdict(OllamaConfig()), **asdict(qwen_3_config)
).with_structured_output(AbusiveResponse)


@before_agent(can_jump_to=["end"])
def check_abusive_service(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Deterministic Guardrail to deny service if user is abusive."""
    print("Checking for abusive content...")
    last_human_message = next(
        (message.content for message in state["messages"][::-1] if message.type == "human"),
        None,
    )

    if not last_human_message:
        return None

    print("Last human message:", last_human_message)
    prompt = abusive_checker_prompt.format(user_message=last_human_message)

    result = abusive_detector.invoke(prompt)
    print("Abusive check result:", result)
    if result.abusive or result.inappropriate_sexual_request:
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "Service denied. Your message was classified as abusive. "
                        f"Category: {result.category}, Target: {result.target}, "
                        f"Confidence: {result.confidence:.2f}. Rationale: {result.rationale}"
                    ),
                }
            ],
            "jump_to": "end",
        }
    return None
