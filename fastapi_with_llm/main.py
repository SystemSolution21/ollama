from fastapi import FastAPI, Depends, HTTPException, Header
import requests
from ollama import chat, ChatResponse
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Get API Key Credits
API_KEY_CREDITS: dict[str | None, int] = {os.getenv(key="API_KEY"): 5}

# Create API Application
app = FastAPI()


# Verify API key
def verify_api_key(api_key: str = Header(default=None)) -> str:
    credits: int = API_KEY_CREDITS.get(api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API key, or no credits.")
    return api_key


# Generate LLM Response
@app.post(path="/gen_llm_res")
def gen_llm_res(prompt: str, api_key=Depends(dependency=(verify_api_key))):

    # Decrement Credit
    API_KEY_CREDITS[api_key] -= 1

    # LLM Response
    response: ChatResponse = chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]
