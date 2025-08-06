# Ollama

## Locally installed ollama models

- gemma3:4b
- nomic-embed-text:latest
- llama3.2:3b
- deepseek-r1:14b
- qwen3:latest

## Open WebUI

### Manual Installation

- .webui_secret_key file auto created
- $ uv pip install open-webui
- $ open-webui serve
- <http://localhost:8080/auth>

## Docker containerized installation for Open-WebUI:main(ollama locally installed)

- docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

## Magentic-UI

- $ uv pip install magentic-ui
- requires docker installed and running
- $ magentic ui --port 8081
- <http://localhost:8081/>
