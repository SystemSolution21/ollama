import streamlit as st
from ollama import chat, ChatResponse

# Set llm model
model: str = "llama3.2:3b"
model: str = "openthinker:7b"
model: str = "deepseek-r1:14b"

# Set page config
st.set_page_config(page_title="Streamlit-Ollama-llm", page_icon="🐋")

# Display title
st.title(body="Ollama LLM Application")


# Generate llm response
def generate_llm_response(prompt: str) -> None:
    """Send user input text to llm model and display response content.

    Args:
        prompt (str): User text input.
    """
    response: ChatResponse = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Display response
    st.info(body=response["message"]["content"])


def main() -> None:
    """Setting form text area for user input text,
    submit button to send message to llm.
    """
    with st.form(key="chat_form"):
        prompt: str = st.text_area(
            label="Enter text! Ask any question and press 'Submit' button.",
            value="",
        )

        submitted: bool = st.form_submit_button(label="Submit")

        if submitted:
            generate_llm_response(prompt=prompt)


if __name__ == "__main__":
    main()
