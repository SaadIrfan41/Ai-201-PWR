import os
from dotenv import load_dotenv
from agents import Agent, Runner,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")




async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent.",
         model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    )

    result = await Runner.run(agent, input="Tell me about recursion in programming.")
    print(result.final_output)


def main_wrapper():
    import asyncio
    asyncio.run(main())