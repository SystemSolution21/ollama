from ollama import chat, ChatResponse

# Set llm model
model: str = "llama3.2:3b"


def main(prompt: str) -> ChatResponse:
    """Send user input text to llm model and return response content.

    Args:
        prompt (str): User text input.

    Returns:
        ChatResponse: Response content.
    """
    # Create Chat
    response: ChatResponse = chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":

    result: ChatResponse = main(prompt="Why is the sky blue?")

    # Output result
    print(result)
