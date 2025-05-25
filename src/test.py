from pydantic import BaseModel
from agents import Agent, Runner
from dotenv import load_dotenv
from agents import (set_tracing_disabled,function_tool)
import os
from agents.extensions.models.litellm_model import LitellmModel

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



@function_tool
def get_weather_data(location: str) -> dict:
    return {
        "location": location,
        "temperature_c": 25.0,
        "summary": "Sunny with light winds"
    }

class WeatherAnswer(BaseModel):
  location: str
  temperature_c: float
  summary: str


agent = Agent(
    name="WeatherToolAgent",
    instructions="Use the get_weather_data tool to fetch current weather and return it.Also return a structured response.",
    tools=[get_weather_data],
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),

    output_type=WeatherAnswer 
)
  
async def get_weather(location: str) -> WeatherAnswer:
  weather_data = await Runner.run(
    agent,
    input=f"Get the weather for {location}",
  )
  return weather_data.final_output
  
if __name__ == "__main__":
  import asyncio
  location = "Peshawar"
  weather = asyncio.run(get_weather(location))
  print(weather)