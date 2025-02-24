from ollama import chat, ChatResponse

# Create Chat
response: ChatResponse = chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": "Why is the sky blue?"},
    ],
)

# Output result
print(response["message"]["content"])
