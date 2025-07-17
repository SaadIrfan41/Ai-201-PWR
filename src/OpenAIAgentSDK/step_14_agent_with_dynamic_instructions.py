import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents import set_tracing_disabled
from agents.run_context import RunContextWrapper
from agents.extensions.models.litellm_model import LitellmModel
from pydantic import BaseModel

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


class UserContext(BaseModel):
    id: str
    age: int
    name: str


def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."


user_info = UserContext(name="Saad", id="123", age=20)


async def main():
    agent = Agent[UserContext](
        name="Assistant",
        instructions=dynamic_instructions,
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hello, What is the age of the user?",
        context=user_info,
    )
    print("Assistant:", result.final_output)


def main_wrapper():
    import asyncio

    asyncio.run(main())
