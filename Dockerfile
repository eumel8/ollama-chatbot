FROM docker.io/ollama/ollama:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew vim-tiny python3-venv python3-pip net-tools curl

COPY . /home/appuser/

RUN pip install -r /home/appuser/requirements.txt
RUN useradd --create-home appuser
RUN ollama serve & sleep 5 && ollama pull nomic-embed-text && ollama pull deepseek-r1:7b
WORKDIR /home/appuser
USER appuser
ENV PYTHONUNBUFFERED=0
ENTRYPOINT ollama serve
