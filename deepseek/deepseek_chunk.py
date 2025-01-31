import sys
from typing import Iterator
import ollama

# Create Chat Response
chat_response: Iterator[ollama.ChatResponse] = ollama.chat(
    model="deepseek-r1:14b",
    messages=[{"role": "user", "content": "Solve quadratic equation x^2+5x+6=0?"}],
    stream=True,
)

# Chat Response stream buffer
reasoning_content: str = ""
content: str = ""

for chunk in chat_response:
    if chunk["message"]["content"]:
        # get the content from the chunk
        chunk_content = chunk["message"]["content"]

        # print the content immediately without newline
        sys.stdout.write(chunk_content)
        sys.stdout.flush()

        # Store in appropriate buffer
        if chunk_content.startswith("<think>"):
            in_thinking: bool = True
        elif chunk_content.startswith("</think>"):
            in_thinking: bool = False
        else:
            if in_thinking:
                reasoning_content += chunk_content
            else:
                content += chunk_content

print(f"\n\nReasoning: ", reasoning_content)
print(f"\nFinal Answer: ", content)
