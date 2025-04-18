from typing import Iterator, Literal
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from ollama import ChatResponse, Client
from dotenv import load_dotenv
import time
import os


# Load Environment Variables
load_dotenv()

# Set llm model
# model: str = "openthinker:7b"
# model: str = "deepseek-r1:14b"
# model: str = "llama3.2:3b"
model: str = "gemma3:4b"

# Set page config
st.set_page_config(page_title="Streamlit-Ollama-Custom-Client-Stream", page_icon="🤖")

# Initialize LLM Client
client: Client = Client(
    host="http://localhost:11434",
    headers={"x-client-key": os.getenv(key="CLIENT_KEY")},
)

st.title(body="Streaming Ollama Chat with Custom Client")

st.write("Hello! How can i assist you today?")

# User input
user_prompt: str = st.text_input(
    label="Ask any question and press 'Submit' button.", value=""
)

# Submit button
submit_btn: bool = st.button(label="Submit")

# Container to display the streaming response
response_container: DeltaGenerator = st.empty()

if submit_btn:
    # Display a message while waiting for the response to start
    response_container.markdown(body="*Thinking...*")

    # Make the API call with streaming enabled
    stream: Iterator[ChatResponse] = client.chat(
        model=model,
        messages=[{"role": "user", "content": user_prompt}],
        stream=True,
    )

    # Initialize an empty string to store the response
    full_response: Literal[""] = ""

    # Process the streaming response
    for chunk in stream:
        if chunk:
            # Extract the text from the chunk
            text_chunk = chunk["message"]["content"]

            # Add the chunk to the full response
            full_response += text_chunk

            # Update the response container with the current text
            response_container.markdown(body=full_response + "▌")

            # # Short delay to make the streaming visible (optional)
            # time.sleep(0.01)

    # Display the final response without the cursor
    response_container.markdown(body=full_response)
