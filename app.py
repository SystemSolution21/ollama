import streamlit as st
import ollama

# Set model
model_deepseek: str = "deepseek-r1:14b"

# Display title
st.title(body="LLM application based on deepseek-r1(run locally)")


# Generate deepseek response
def generate_deepseek_response(promt: str):
    response: ollama.ChatResponse = ollama.chat(
        model=model_deepseek,
        messages=[
            {
                "role": "user",
                "content": promt,
            }
        ],
    )

    # Display response
    st.info(body=response["message"]["content"])


def main() -> None:
    with st.form(key="chat_form"):
        prompt = st.text_area(
            label="Enter text, you can ask a question and press Submit button.",
            value="",
        )

        submitted = st.form_submit_button(label="Submit")

        if submitted:
            generate_deepseek_response(promt=prompt)


if __name__ == "__main__":
    main()
