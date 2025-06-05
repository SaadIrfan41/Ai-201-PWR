import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, RunContextWrapper, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel
from agents.tool import function_tool

set_tracing_disabled(disabled=True)

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )


def student_error_handler(ctx: RunContextWrapper[None], error: Exception) -> str:
    return f"Error looking up student: {str(error)}"


@function_tool
def get_weather(location: str, unit: str = "C") -> str:
    """
    Fetch the weather for a given location, returning a short description.
    """

    # Example logic
    raise ValueError(f"Cannot fetch weather for location: {location}")
    # return f"The weather in {location} is 22 degrees {unit}."


@function_tool
def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers.
    """
    print(f"subtracting {a} and {b}")

    # Example logic
    return a - b


@function_tool(failure_error_function=student_error_handler)
def student_finder(student_roll: int) -> str:
    """
    find the PIAIC student based on the roll number
    """
    data = {1: "Qasim", 2: "Sir Zia", 3: "Daniyal"}

    if student_roll is None or student_roll not in data:
        raise ValueError(f"Student with roll number {student_roll} not found.")
    return data[student_roll]


# Note: Supplying a list of tools doesn't always mean the LLM will use a tool.
# You can force tool use by setting ModelSettings.tool_choice the following options:
# 1: auto, which allows the LLM to decide whether or not to use a tool.
# 2: required, which requires the LLM to use a tool (but it can intelligently decide which tool).
# 3: none, which requires the LLM to not use a tool.
# 4: Setting a specific string e.g. my_tool, which requires the LLM to use that specific tool.


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpfull assistant",
        tools=[get_weather, student_finder, subtract],  # You can add more tools here
        # The output of the first tool call is used as the final output. This
        # means that the LLM does not process the result of the tool call.
        tool_use_behavior="stop_on_first_tool",
        # The default behavior. Tools are run, and then the LLM receives the results
        # and gets to respond.
        # tool_use_behavior='run_llm_again',
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
        model_settings=ModelSettings(tool_choice="subtract"),
    )
    # result = await Runner.run(agent, "Share PIAIC roll number 3 student details.")
    # result = await Runner.run(agent, "Share PIAIC roll number 52 student details.")
    result = await Runner.run(agent, "What is 10 + 5?")
    print(result.last_agent.name)
    print(result.final_output)


def main_wrapper():
    import asyncio

    asyncio.run(main())
