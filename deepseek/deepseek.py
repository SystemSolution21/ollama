from pathlib import Path
import ollama

# Set Model and Prompt
model_deepseek = "deepseek-r1:14b"
prompt = "How to solve quadratic equation x^2+5x+6=0"

# Current directory file path
file_path: Path = Path(__file__).parent

# Ollama ChatResponse
response: ollama.ChatResponse = ollama.chat(
    model=model_deepseek, messages=[{"role": "user", "content": prompt}]
)

deepseek_response = response["message"]["content"]

print(deepseek_response)

# Save response to text file
with open(
    file=file_path / "deepseek_response.txt", mode="w", encoding="utf-8"
) as txt_file:
    txt_file.write(deepseek_response)
