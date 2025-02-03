FROM docker.io/ollama/ollama:latest

RUN ollama serve & sleep 5 && ollama pull nomic-embed-text && ollama pull deepseek-r1:7b
