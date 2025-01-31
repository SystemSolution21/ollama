Ollama Tutorial:
Locally run;
llama3.2:3b
deepseek-r1:14b

Run app.py:
streamlit run path\to\app.py

deepseek_chunk.py:
Set chat response stream=True, write chunk content immediately on sys.stdout.
Collect content inside "<think></think>" in Reasoning and rest in Final Answer
