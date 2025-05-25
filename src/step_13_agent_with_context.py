import os
import random
from dotenv import load_dotenv
from agents import Agent, Runner, TResponseInputItem
from agents import set_tracing_disabled,function_tool
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

# Simulating a DB connection class
class FakeDatabaseConnection:
    def __init__(self):
        self.data = {
            "user_balances": {"user_1": 150.0},
            "store_items": {"apple": 2.5, "banana": 1.0, "milk": 3.0}
        }
    
    def get_store_items(self) -> dict[str, float]:
        return self.data["store_items"]

    def get_balance(self, user_id: str) -> float:
        return self.data["user_balances"].get(user_id, 0.0)

    def search_item(self, name: str) -> float:
        return self.data["items"].get(name, random.uniform(1, 10))
    
# Custom Local Context including DB connection
class AppLocalContext(BaseModel):
    user_id: str
    db: FakeDatabaseConnection
    cart: list[str]
    model_config = {
        "arbitrary_types_allowed": True
    }

@function_tool
async def view_store_items(wrapper: RunContextWrapper[AppLocalContext]) -> dict[str, float]:
    """
    Return all available items in the store with their prices.
    """
    return wrapper.context.db.get_store_items()

@function_tool
async def get_user_balance(wrapper: RunContextWrapper[AppLocalContext]) -> float:
    """
    Get the account balance of the user using the user's ID.
    """
    print("Getting User_ID")
    user_id = wrapper.context.user_id
    return wrapper.context.db.get_balance(user_id)

@function_tool
async def search_item_price(wrapper: RunContextWrapper[AppLocalContext], item: str) -> str:
    """
    Search for an item in the database and return its price.
    """
    print(f"Searching for {item} price")
    price = wrapper.context.db.search_item(item)
    return f"{item} costs ${price:.2f}"

@function_tool
async def add_to_cart(wrapper: RunContextWrapper[AppLocalContext], item: str):
    """
    Add one or more items to the user's shopping cart.
    """
    print(f"Adding {item} to Cart")
    wrapper.context.cart.append(item)

@function_tool
async def view_cart(wrapper: RunContextWrapper[AppLocalContext]) -> list[str]:
    """
    Retrieve the current list of items in the user's shopping cart.
    """
    print("Getting Cart Items")
    return wrapper.context.cart


async def main():
    agent = Agent[AppLocalContext](
        name="Grocery Assistant",
        instructions="""
        You are a helpfull Grocery Assistant.
        If a user ask to find item prices and manage their cart assist them.
        You can add items to the users cart if the ask.
        You can get all the avaliable items in the store if the user ask.
        """,
        tools=[get_user_balance, search_item_price, add_to_cart, view_cart,view_store_items],
        model=LitellmModel(model=str(groq_model), api_key=groq_api_key),
    )

    # Instantiate the context
    context = AppLocalContext(
        user_id="user_1",
        db=FakeDatabaseConnection(),
        cart=[]
    )
    # Simulate a conversation
    conversation: list[TResponseInputItem] = []
    print("You are now chatting with your grocery assistant. Type 'exit' to end.")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        conversation.append({"role": "user", "content": user_input})

        result = await Runner.run(agent, conversation, context=context)

        print("Assistant:", result.final_output)

        conversation = result.to_input_list()



def main_wrapper():
    import asyncio

    asyncio.run(main())