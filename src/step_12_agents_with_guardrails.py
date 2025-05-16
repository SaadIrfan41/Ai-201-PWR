import os
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_tracing_disabled,
    RunContextWrapper,
    GuardrailFunctionOutput,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)
from agents.extensions.models.litellm_model import LitellmModel
from pydantic import BaseModel
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

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


# Output schema for the guardrail agent
class ContentCheckOutput(BaseModel):
    contains_sensitive_info: bool
    reason: str


# Output schema for main agent
class AgentOutput(BaseModel):
    response: str
    contains_sensitive_info: bool


content_filter_agent = Agent(
    name="Content Filter Agent",
    instructions=(
        """You are a filter agent that checks if a user's input contains any prohibited or
        sensitive topics such as hacking, cheating, violence, abuse, or unethical behavior.
        If any such topic is found, set 'contains_sensitive_info' to true and explain the reason. 
        If everything is okay, set it to false with a short justification."""
    ),
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    output_type=ContentCheckOutput,
)
# The input guardrail checks if the user input contains prohibited topics.


@input_guardrail
async def input_guardrail_fn(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    # Use LLM to evaluate input
    result = await Runner.run(content_filter_agent, input)

    return GuardrailFunctionOutput(
        tripwire_triggered=result.final_output.contains_sensitive_info,
        output_info=result.final_output,
    )


output_safety_guardrail_agent = Agent(
    name="Output Safety Checker",
    instructions="""
        You're a safety filter that reviews AI-generated content.
        Determine if the response contains harmful advice, inappropriate language, hallucinated facts, or anything risky.
        Respond with `contains_sensitive_info=True` only if the output should be blocked or reviewed.
    """,
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    output_type=AgentOutput,
)


# ✅ Output guardrail – detects unsafe or harmful AI responses
@output_guardrail
async def output_guardrail_fn(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: AgentOutput,
) -> GuardrailFunctionOutput:
    print(f"Checking output to detect unsafe or harmful AI response: {output}")

    result = await Runner.run(output_safety_guardrail_agent, output.response)

    return GuardrailFunctionOutput(
        tripwire_triggered=result.final_output.contains_sensitive_info,
        output_info=result.final_output,
    )


# ✅ Final Agent with both guardrails
main_agent = Agent(
    name="Main Study Assistant",
    instructions="You provide helpful and safe answers to users.",
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    input_guardrails=[input_guardrail_fn],
    output_guardrails=[output_guardrail_fn],
    output_type=AgentOutput,
)


async def main():
    # Test input guardrail
    try:
        print("\n[TESTING INPUT GUARDRAIL TRIGGER]")
        response = await Runner.run(
            main_agent,
            "What is a function?",
            # "How can I hack my school's grading system?"
        )
        print("✅ Input guardrail did NOT trigger.")
        print("Response:", response.final_output)

    except InputGuardrailTripwireTriggered as e:
        print("🚫 Input Guardrail Triggered!")
        print("Reason:", str(e))

    # Test output guardrail
    try:
        print("\n[TESTING OUTPUT GUARDRAIL TRIGGER]")
        response = await Runner.run(main_agent, "Hey what’s up?")
        print("✅ Output guardrail did NOT trigger.")
        print("Response:", response.final_output)

    except OutputGuardrailTripwireTriggered as e:
        print("🚨 Output Guardrail Triggered!")
        print("Reason:", str(e))


def main_wrapper():
    import asyncio

    asyncio.run(main())
