from pydantic import BaseModel
from agents import Agent, Runner
from dotenv import load_dotenv
from agents.run_context import RunContextWrapper
from agents.lifecycle import AgentHooks, RunHooks


from agents import set_tracing_disabled, function_tool
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


# ✅ Agent-specific lifecycle hooks
class CustomAgentHooks(AgentHooks):
    async def on_start(self, context: RunContextWrapper, agent):
        print(
            f"[AgentHook] Agent '{agent.name}' started with context: {context.context}"
        )

    async def on_end(self, context: RunContextWrapper, agent, output):
        print(f"[AgentHook] Agent '{agent.name}' finished with output: {output}")

    async def on_handoff(self, context: RunContextWrapper, agent, source):
        print(f"[AgentHook] Agent '{agent.name}' received handoff from '{source.name}'")

    async def on_tool_start(self, context: RunContextWrapper, agent, tool):
        print(
            f"[AgentHook] Tool '{tool.name}' is about to be used by agent '{agent.name}'"
        )

    async def on_tool_end(self, context: RunContextWrapper, agent, tool, result):
        print(f"[AgentHook] Tool '{tool.name}' finished with result: {result}")


# ✅ Run-wide lifecycle hooks
class CustomRunHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent):
        print(f"[RunHook] Agent '{agent.name}' is about to be invoked.")

    async def on_agent_end(self, context: RunContextWrapper, agent, output):
        print(f"[RunHook] Agent '{agent.name}' completed with output: {output}")

    async def on_handoff(self, context: RunContextWrapper, from_agent, to_agent):
        print(f"[RunHook] Handoff from '{from_agent.name}' to '{to_agent.name}'")

    async def on_tool_start(self, context: RunContextWrapper, agent, tool):
        print(f"[RunHook] Tool '{tool.name}' is starting under agent '{agent.name}'")

    async def on_tool_end(self, context: RunContextWrapper, agent, tool, result):
        print(f"[RunHook] Tool '{tool.name}' finished with result: {result}")


spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    hooks=CustomAgentHooks(),
    tools=[
        spanish_agent.as_tool(
            tool_name="spanish_agent",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)


async def main():
    result = await Runner.run(
        orchestrator_agent,
        input="Say 'Hello, how are you?' in Spanish.",
        hooks=CustomRunHooks(),
    )
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


# @function_tool
# def get_weather_data(location: str) -> dict:
#     return {
#         "location": location,
#         "temperature_c": 25.0,
#         "summary": "Sunny with light winds"
#     }

# class WeatherAnswer(BaseModel):
#   location: str
#   temperature_c: float
#   summary: str


# agent = Agent(
#     name="WeatherToolAgent",
#     instructions="Use the get_weather_data tool to fetch current weather and return it.Also return a structured response.",
#     tools=[get_weather_data],
#     model=LitellmModel(model=str(groq_model), api_key=groq_api_key),

#     output_type=WeatherAnswer
# )

# async def get_weather(location: str) -> WeatherAnswer:
#   weather_data = await Runner.run(
#     agent,
#     input=f"Get the weather for {location}",
#   )
#   return weather_data.final_output

# if __name__ == "__main__":
#   import asyncio
#   location = "Peshawar"
#   weather = asyncio.run(get_weather(location))
#   print(weather)
