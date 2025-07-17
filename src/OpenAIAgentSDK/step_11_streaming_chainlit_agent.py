# Run this file "uv run chainlit run src/step_11_streaming_chainlit_agent.py -w"

import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from openai.types.responses import ResponseTextDeltaEvent
# Load environment variables from .env file

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


@cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    )
    cl.user_session.set("agent", agent)

    await cl.Message(content="Welcome! How can I help you today?").send()



@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    # Create a new message object for streaming
    msg = cl.Message(content="")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        # Run the agent with streaming enabled
        result = Runner.run_streamed(agent, history)

        # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                token = event.data.delta
                await msg.stream_token(token)

        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
