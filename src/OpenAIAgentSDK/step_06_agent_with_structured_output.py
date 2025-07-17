import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from pydantic import BaseModel

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )


class TravelPlan(BaseModel):
    destination: str
    days: int
    activities: list[str]
    estimated_cost: float


async def main():
    travel_agent = Agent(
        name="Travel Planner Agent",
        instructions=(
            """You are an agent that creates travel plans. 
            You will be given the name of a destination.
            Your job is to return a structured plan including number of days,
            popular activities, and estimated cost."""
        ),
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
        output_type=TravelPlan,
    )

    result = await Runner.run(travel_agent, input="Tokyo, Japan")
    print(result.final_output.model_dump())


def main_wrapper():
    import asyncio

    asyncio.run(main())
