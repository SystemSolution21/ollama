from ollama import chat, ChatResponse


def main(prompt: str) -> ChatResponse:

    # Create Chat
    response: ChatResponse = chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":

    result: ChatResponse = main(prompt="Why is the sky blue?")

    # Output result
    print(result)
