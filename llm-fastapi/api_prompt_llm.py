import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Set url endpoints
url: str = "http://127.0.0.1:8000/gen_llm_res"

# Set API key in headers
headers = {
    "x-api-key": os.getenv(key="API_KEY"),
    "Content-Type": "application/json",
}

# Get response
payload = {"prompt": "Explain about FastAPI"}
response: requests.Response = requests.post(url=url, headers=headers, json=payload)
response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

# Output response
print(response.json())

# Save response to text file
file_path: Path = Path(__file__).parent
with open(file=file_path / "ai_response.txt", mode="w", encoding="utf-8") as f:
    f.write(response.json()["response"])
