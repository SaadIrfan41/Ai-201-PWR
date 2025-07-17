import os
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_tracing_disabled,
    RunContextWrapper,
    handoff,
    function_tool,
)
from agents.extensions.models.litellm_model import LitellmModel
from pydantic import BaseModel
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


# Load the environment variables from the .env file
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


class CoachEscalation(BaseModel):
    concern: str  # What the user is worried about
    reason: str  # Why the assistant couldn’t help


@function_tool
def log_concern(concern: str):
    """
    Log a concern for future help.
    """
    print(f"Logging concern: {concern}")
    return "Concern logged. Case ID: 001"


async def main():
    career_coach = Agent(
        name="Career Coach",
        handoff_description="Handles complex job seeker concerns requiring expert advice",
        instructions=prompt_with_handoff_instructions("""
            You are a Career Coach Adviser.
            Advice the user based on the concern.
            If the concern involves visa issues you must call the 'log_concern' tool 
            and return the ID returned by the tool function """),
        tools=[log_concern],
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    )

    async def on_escalate(ctx: RunContextWrapper[None], input: CoachEscalation):
        print("Escalating to career coach: ", input.concern)
        print("Reason for escalation: ", input.reason)

    resume_assistant = Agent(
        name="Resume Assistant",
        instructions=(
            "You help users write resumes and cover letters. "
            + "If the user's concern is too complex (e.g., gaps, visas), escalate to a Career Coach"
        ),
        handoffs=[
            handoff(
                agent=career_coach,
                input_type=CoachEscalation,
                on_handoff=on_escalate,
            )
        ],
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    )
    input = "I have a 5-year employment gap due to illness, what should I do?"
    # input = "I'm an international student with no work visa yet, but I want a job in the US. Can you help?"
    # input = "I’m changing careers from teaching to marketing. What should I highlight on my resume?"

    result = await Runner.run(resume_assistant, input)
    print(result.final_output)


def main_wrapper():
    import asyncio

    asyncio.run(main())
