from langgraph_sdk import get_client
from langgraph.types import RunnableConfig
from dotenv import load_dotenv
import yaml
load_dotenv()


# This can be a local or remote deployment URL, but it must point to a Langgraph Server
langgraph_api = "http://localhost:2024"

# Initialize the client that will handle all API requests to the Langgraph Server
client = get_client(url=langgraph_api)

def load_llm_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    for llm_type, params in config["llms"].items():
        if params.get("enabled"):
            llm_config = {"llm_type": llm_type}
            llm_config.update({k: v for k, v in params.items() if k != "enabled"})
            return llm_config
    raise ValueError("No enabled LLM found in config.")

async def create_user_thread(user_id: str):
    """Create a new thread for a user."""
    thread = await client.threads.create(
        if_exists="do_nothing",
        metadata={
            "user_id": user_id,
        }
    )
    return thread


async def send_message(thread_id: str, question: str, llm_config: dict, user_config: dict = None):
    """Send a message to the assistant and wait for response."""
    input_data = {
        "question": question,
        "llm_config": llm_config
    }

    config = None
    if user_config:
        config = RunnableConfig(configurable={"user": user_config})

    response = await client.runs.wait(
        thread_id=thread_id,
        assistant_id="ChatAgent",
        input=input_data,
        config=config,
    )

    return response


async def main():
    """Main function to run the frontend."""
    user_id = "Fays"

    # Load LLM configuration
    llm_config = load_llm_config("llm_config.yaml")

    # Create a thread for the user
    thread = await create_user_thread(user_id)
    print(f"Thread created: {thread}")

    # User configuration
    user_config = {
        "user_id": user_id,
        "name": "Fays",
    }

    # Send a message and get response
    response = await send_message(
        thread_id=thread["thread_id"],
        question="What's the user's name?",
        llm_config=llm_config,
        user_config=user_config
    )

    print(f"Response: {response}")


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())