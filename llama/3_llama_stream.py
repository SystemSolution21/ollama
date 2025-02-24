from typing import Iterator
from ollama import chat, ChatResponse


def main(prompt: str) -> None:
    # Create Chat Stream
    stream: Iterator[ChatResponse] = chat(
        model="llama3.2:3b",
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
