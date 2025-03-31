stOllama:
llama3.2:3b
deepseek-r1:14b
openthinker:7b

deepseek:
deepseek_chunk.py;
Set chat response stream=True, write chunk content immediately on sys.stdout.
Collect content inside "<think></think>" in Reasoning and rest in Final Answer

streamlit:
$ streamlit run app.py

FastAPI:
$ uvicorn main:app --reload

Open WebUI:
.webui_secret_key
$ open-webui serve
http://localhost:8080/auth
