from dataclasses import asdict
from typing import Any, Literal

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.chat_models import BaseChatModel, init_chat_model
from pydantic import BaseModel

# from rich import print  # pylint: disable=redefined-builtin
from src.configs import AWSConfig, nova_micro_config


class DerivedMood(BaseModel):
    user_mood: Literal["happy", "sad", "angry", "neutral"]
    reason: Literal["agent", "other"]


mood_decider: BaseChatModel = init_chat_model(
    **asdict(AWSConfig()),
    **asdict(nova_micro_config),
).with_structured_output(DerivedMood)


class UserMood(AgentState):
    """State to track the user's mood."""

    user_mood: dict


class MoodMiddleware(AgentMiddleware):
    """Middleware to update and respond based on user's mood."""

    state_schema = UserMood

    def before_model(self, state: UserMood, runtime) -> dict[str, Any] | None:
        last_message = next(
            (message.content for message in state["messages"][::-1] if message.type == "human"),
            None,
        )
        if not last_message:
            return None
        mood = mood_decider.invoke(
            f"""
                You are a strict mood classification agent.

                Determine the user's emotional mood based on the following message:
                "{last_message}"

                Rules:
                - Choose exactly ONE mood from: happy, sad, angry, neutral
                - Determine whether the mood is caused by the agent or by external reasons
                - Use 'agent' if the mood is caused by the assistant’s mistake or behaviour. Or if the user directly blames the agent.
                - Use 'other' if the mood is caused by external circumstances

                Output requirements:
                - Respond with a Python-style dictionary only
                - Use exactly these keys: 'user_mood', 'reason'
                - 'user_mood' must be one of: happy, sad, angry, neutral
                - 'reason' must be one of: agent, other
                - Do NOT include explanations, comments, or extra text

                Examples:

                    User: "Thanks, that worked perfectly!"
                    Output: {{'user_mood': 'happy', 'reason': 'other'}}

                    User: "I’m disappointed — the deadline got delayed again."
                    Output: {{'user_mood': 'sad', 'reason': 'other'}}

                    User: "This is frustrating. You gave me the wrong instructions."
                    Output: {{'user_mood': 'angry', 'reason': 'agent'}}

                    User: "That’s not what I asked for."
                    Output: {{'user_mood': 'angry', 'reason': 'agent'}}

                    User: "Alright, noted. Let’s continue."
                    Output: {{'user_mood': 'neutral', 'reason': 'other'}}

                    User: "I’m upset because your solution didn’t work."
                    Output: {{'user_mood': 'sad', 'reason': 'agent'}}
            """
        )

        runtime.stream_writer(mood.model_dump())
        return {"user_mood": mood.model_dump()}
