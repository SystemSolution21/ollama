from ollama import ChatResponse, Client
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()


# llama client chat
def llama_client_chat(prompt: str):
    try:
        # Initialize client with custom host and headers
        client: Client = Client(
            host="http://localhost:11434",
            headers={"x-client-key": os.getenv(key="CLIENT_KEY")},
        )

        # Define chat messages
        messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]

        # Send the chat request to custom client
        response: ChatResponse = client.chat(model="llama3.2:3b", messages=messages)

        # Extract and print the response
        print("\nModel Response:")
        print("--------------")
        print(response.message.content)

        # Print additional response metadata
        print("\nResponse Metadata:")
        print("-----------------")
        print(f"Model: {response.model}")
        print(f"Created At: {response.created_at}")
        print(f"Total Duration: {response.total_duration}ms")
        print(f"Load Duration: {response.load_duration}ms")
        print(f"Prompt Eval Count: {response.prompt_eval_count}")
        print(f"Eval Count: {response.eval_count}")

    except Exception as e:
        print(f"An error occurred: {str(object=e)}")


if __name__ == "__main__":
    llama_client_chat(prompt="Explain about Ollama Client Library.")
