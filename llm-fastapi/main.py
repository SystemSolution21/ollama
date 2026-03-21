import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from ollama import AsyncClient, ChatResponse
from pydantic import BaseModel

# Load Environment Variables
load_dotenv()

# Get API Key Credits
API_KEY: str | None = os.getenv(key="API_KEY")
API_KEY_CREDITS: dict[str, int] = {}
LLM_MODEL: str = os.getenv(key="LLM_MODEL", default="llama3.2:latest")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate environment variables and initialize credits on startup."""
    if not API_KEY:
        raise ValueError("API_KEY environment variable not set.")
    API_KEY_CREDITS[API_KEY] = 5
    yield


# Create API Application
app = FastAPI(lifespan=lifespan)


class PromptRequest(BaseModel):
    """Pydantic model for request body."""

    prompt: str


class LLMResponse(BaseModel):
    """Pydantic model for LLM response."""

    response: str


# Verify API key
async def verify_api_key(x_api_key: str = Header(default=None)) -> str:
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API Key header")
    credits: int = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key or no credits remaining.",
        )
    return x_api_key


# Generate LLM Response
@app.post("/gen_llm_res", response_model=LLMResponse)
async def gen_llm_res(request: PromptRequest, x_api_key: str = Depends(verify_api_key)):

    # Decrement Credit
    API_KEY_CREDITS[x_api_key] -= 1

    # LLM Response
    response: ChatResponse = await AsyncClient().chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": request.prompt},
        ],
    )

    return LLMResponse(response=response["message"]["content"])
