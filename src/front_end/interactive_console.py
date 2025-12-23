import uuid

from langchain.messages import HumanMessage
from rich import print  # pylint: disable=redefined-builtin


# Interactive console loop
def interactive_console(agent):
    """Run an interactive console chat with the agent."""
    thread_id = str(uuid.uuid4())  # Unique conversation thread
    config = {"configurable": {"thread_id": thread_id}}
    print("Interactive Agent Console (type 'exit' to quit)")
    print("-" * 50)
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        # Exit condition
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        if not user_input:
            continue
        # Send message to agent
        try:
            result = agent.invoke({"messages": [HumanMessage(content=user_input)]}, config)

            # Display agent response
            last_message = result["messages"][-1]
            print(f"\nAgent: {last_message.content}")
        except Exception as e:
            print(f"\nError: {e}")
