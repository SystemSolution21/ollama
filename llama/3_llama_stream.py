import os
from typing import Iterator

from dotenv import load_dotenv
from ollama import ChatResponse, chat

load_dotenv()

# Get LLM Model Name
LLM_MODEL: str = os.getenv(key="LLM_MODEL", default="llama3.2:latest")


def main(prompt: str) -> None:
    # Create Chat Stream
    stream: Iterator[ChatResponse] = chat(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    # Output stream
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)


if __name__ == "__main__":
    main(prompt="Explain about Ollama chat library.")
