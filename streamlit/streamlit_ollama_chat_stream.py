from typing import Iterator, Literal
import streamlit as st
from ollama import chat, ChatResponse
from streamlit.delta_generator import DeltaGenerator

# Set llm model
# model: str = "llama3.2:3b"
# model: str = "openthinker:7b"
# model: str = "deepseek-r1:14b"
model: str = "gemma3:4b"

# Set page config
st.set_page_config(page_title="Streamlit-Ollama-Chat-Stream", page_icon="🐋")

# Display title
st.title(body="Streamlit Ollama Chat Stream")

# Setting form text area for user input text,
# submit button to send message to llm.
with st.form(key="chat_form"):
    prompt: str = st.text_area(
        label="Enter text! Ask any question and press 'Submit' button.",
        value="",
    )
    submitted: bool = st.form_submit_button(label="Submit")

# Container to display the chat streaming - placed after the form
stream_container: DeltaGenerator = st.empty()


# Generate llm chat stream
def generate_llm_chat_stream(prompt: str) -> None:
    """Send user input text to llm model and display response content.

    Args:
        prompt (str): User text input.
    """
    stream: Iterator[ChatResponse] = chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=True,
    )

    # Store the stream response
    stream_response: Literal[""] = ""

    # Process the stream response
    for chunk in stream:
        if chunk is not None:
            # Extract the text from the chunk
            stream_response += chunk["message"]["content"]

            # Update the response container with the current text
            stream_container.markdown(body=stream_response + "▌")

    # Display the final response without the cursor
    stream_container.markdown(body=stream_response)


def main() -> None:
    if submitted:
        # Display a message while waiting for the response to start
        stream_container.markdown(body="*Thinking...*\n\n")

        # Generate llm stream response
        generate_llm_chat_stream(prompt=prompt)


if __name__ == "__main__":
    main()
