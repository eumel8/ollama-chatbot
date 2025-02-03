FROM docker.io/ollama/ollama:latest

RUN ollama serve & sleep 5 && ollama pull nomic-embed-text && ollama pull deepseek-r1:7b
#RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull mistral:7b
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew vim-tiny python3-venv python3-pip net-tools curl

COPY . /home/appuser/

RUN pip install -r /home/appuser/requirements.txt
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
ENV PYTHONUNBUFFERED=0
