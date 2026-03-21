import asyncio
import os

from dotenv import load_dotenv
from ollama import AsyncClient

# Load Environment Variables
load_dotenv()

# Get LLM Model Name
LLM_MODEL: str = os.getenv(key="LLM_MODEL", default="llama3.2:latest")


# Asynchronous Ollama Client Chat
async def llama_async_client(prompt: str):
    try:
        client_key: str | None = os.getenv(key="CLIENT_KEY")
        if client_key:
            # Initialize Asynchronous client with custom host and headers
            async_client = AsyncClient(
                host="http://localhost:11434",
                headers={"x-client-key": client_key},
            )

            # Send chat messages to Asynchronous Client
            async for chunk in await async_client.chat(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            ):
                # Output model response
                print(chunk["message"]["content"], end="", flush=True)

    except Exception as e:
        print(f"An error occurred: {str(object=e)}")


if __name__ == "__main__":
    asyncio.run(
        main=llama_async_client(prompt="Explain about Ollama AsyncClient Library.")
    )
