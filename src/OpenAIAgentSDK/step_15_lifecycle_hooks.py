import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled
from agents.run_context import RunContextWrapper
from agents.extensions.models.litellm_model import LitellmModel
from agents.lifecycle import AgentHooks, RunHooks
from pydantic import BaseModel

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")
set_tracing_disabled(disabled=True)

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")
if not groq_model:
    raise ValueError("GROQ_MODEL is not set in the .env file.")


# User context
class UserContext(BaseModel):
    id: str
    age: int
    name: str


# Dynamic instructions
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."


# ✅ Agent-specific lifecycle hooks
class CustomAgentHooks(AgentHooks[UserContext]):
    async def on_start(self, context: RunContextWrapper[UserContext], agent):
        print(
            f"[AgentHook] Agent '{agent.name}' started with context: {context.context}"
        )

    async def on_end(self, context: RunContextWrapper[UserContext], agent, output):
        print(f"[AgentHook] Agent '{agent.name}' finished with output: {output}")

    async def on_handoff(self, context: RunContextWrapper[UserContext], agent, source):
        print(f"[AgentHook] Agent '{agent.name}' received handoff from '{source.name}'")

    async def on_tool_start(self, context: RunContextWrapper[UserContext], agent, tool):
        print(
            f"[AgentHook] Tool '{tool.name}' is about to be used by agent '{agent.name}'"
        )

    async def on_tool_end(
        self, context: RunContextWrapper[UserContext], agent, tool, result
    ):
        print(f"[AgentHook] Tool '{tool.name}' finished with result: {result}")


# ✅ Run-wide lifecycle hooks
class CustomRunHooks(RunHooks[UserContext]):
    async def on_agent_start(self, context: RunContextWrapper[UserContext], agent):
        context.context.name = "Khubaib"  # ✅ Modify context here

        print(f"[RunHook] Agent '{agent.name}' is about to be invoked.")

    async def on_agent_end(
        self, context: RunContextWrapper[UserContext], agent, output
    ):
        print(f"[RunHook] Agent '{agent.name}' completed with output: {output}")

    async def on_handoff(
        self, context: RunContextWrapper[UserContext], from_agent, to_agent
    ):
        print(f"[RunHook] Handoff from '{from_agent.name}' to '{to_agent.name}'")

    async def on_tool_start(self, context: RunContextWrapper[UserContext], agent, tool):
        print(f"[RunHook] Tool '{tool.name}' is starting under agent '{agent.name}'")

    async def on_tool_end(
        self, context: RunContextWrapper[UserContext], agent, tool, result
    ):
        print(f"[RunHook] Tool '{tool.name}' finished with result: {result}")


# Sample context
user_info = UserContext(name="Saad", id="123", age=20)


# Main async function
async def main():
    agent = Agent[UserContext](
        name="Assistant",
        instructions=dynamic_instructions,
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
        hooks=CustomAgentHooks(),
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hello, What is the age of the user?",
        context=user_info,
        hooks=CustomRunHooks(),
    )
    print("Assistant:", result.final_output)


# Sync wrapper
def main_wrapper():
    import asyncio

    asyncio.run(main())
