import requests
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Set url for uvicorn server
url: str = "http://127.0.0.1:8000/gen_llm_res?prompt=Tell me about Python"

# Set AIP key in headers
headers = {"api-key": os.getenv(key="API_KEY"), "Content-Type": "application/json"}

# Get response
response = requests.post(url=url, headers=headers)

# Output result
print(response.json())
