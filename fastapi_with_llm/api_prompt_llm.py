from typing import Any
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load Environment Variables
load_dotenv()

# Set url for uvicorn server
url: str = "http://127.0.0.1:8000/gen_llm_res?prompt=Explain about FastAPI"

# Set AIP key in headers
headers = {
    "x-api-key": os.getenv(key="API_KEY"),
    "Content-Type": "application/json",
}

# Get response
response: requests.Response = requests.post(url=url, headers=headers)

# Output response
print(response.json())

# Save response to text file
file_path: Path = Path(__file__).parent
with open(file=file_path / "ai_response.txt", mode="w", encoding="utf-8") as file:
    file.write(response.json())
