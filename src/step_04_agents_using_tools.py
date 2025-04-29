import os
from dotenv import load_dotenv
from agents import Agent, Runner,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.tool import function_tool
set_tracing_disabled(disabled=True)

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@function_tool
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."

@function_tool
def student_finder(student_roll: int) -> str:
  """
  find the PIAIC student based on the roll number
  """
  data = {1: "Qasim",
          2: "Sir Zia",
          3: "Daniyal"}

  return data.get(student_roll, "Not Found")

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpfull Assistant",
        tools=[get_weather, student_finder], # add tools here
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    )
    result = await Runner.run(agent, "Share PIAIC roll number 3 student details.")
    print(result.last_agent.name)
    print(result.final_output)

def main_wrapper():
    import asyncio
    asyncio.run(main())

    