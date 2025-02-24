import asyncio
from typing import AsyncIterator
from ollama import AsyncClient, ChatResponse
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()


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
                model="llama3.2:3b",
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
