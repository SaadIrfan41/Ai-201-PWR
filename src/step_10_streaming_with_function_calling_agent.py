import os
import asyncio
import random
from dotenv import load_dotenv
from agents import Agent, Runner, ItemHelpers, set_tracing_disabled
from agents.tool import function_tool
from agents.extensions.models.litellm_model import LitellmModel


# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY is not set. Please ensure it is defined in your .env file."
    )
if not groq_model:
    raise ValueError(
        "GROQ_MODEL is not set. Please ensure it is defined in your .env file."
    )


# === FUNCTION TOOL ===
@function_tool
def how_many_jokes() -> int:
    """Return a random number between 1 and 5"""
    return random.randint(1, 5)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key)

    )

    result = Runner.run_streamed(agent, input="Hello!")

    print("=== Run starting ===")
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue  # Skip token deltas here
        elif event.type == "agent_updated_stream_event":
            print(f"[Agent updated: {event.new_agent.name}]")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print("-- Agent response:")
                print(ItemHelpers.text_message_output(event.item))
    print("=== Run complete ===")


def main_wrapper():
    asyncio.run(main())
