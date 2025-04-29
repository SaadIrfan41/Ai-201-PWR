import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )


async def main():
    history_tutor_agent = Agent(
        name="History Tutor",
        handoff_description="Specialist agent for historical questions",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    )

    math_tutor_agent = Agent(
        name="Math Tutor",
        handoff_description="Specialist agent for math questions",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    )

    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        handoffs=[history_tutor_agent, math_tutor_agent],
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    )

    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)


def main_wrapper():
    import asyncio

    asyncio.run(main())
