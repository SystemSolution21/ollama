from pathlib import Path
import ollama

# Current directory file path
file_path: Path = Path(__file__).parent

# Set Model and Prompt
model_llama = "llama3.2:3b"
prompt = "How to solve quadratic equation x^2+5x+6=0"

# Ollama ChatResponse
response: ollama.ChatResponse = ollama.chat(
    model=model_llama, messages=[{"role": "user", "content": prompt}]
)

llama_response = response["message"]["content"]

# Print response
print(llama_response)

# Save ollama response in text file
with open(
    file=file_path / "llama_response.txt", mode="w", encoding="utf-8"
) as txt_file:
    txt_file.write(llama_response)
