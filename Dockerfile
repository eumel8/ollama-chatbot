FROM docker.io/ollama/ollama:latest as base

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew vim-tiny python3-venv python3-pip net-tools curl

COPY . /home/appuser/
COPY --from=base /bin /usr/bin
COPY --from=base /lib/ollama/*.so /usr/lib/ollama/
COPY --from=base /lib/ollama/cuda_v11 /usr/lib/ollama/cuda_v11

RUN pip install -r /home/appuser/requirements.txt
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
ENV PYTHONUNBUFFERED=0
# fetch of the models will produce a very big image
# RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull mistral:7b
# RUN ollama serve & sleep 5 && ollama pull nomic-embed-text && ollama pull deepseek-r1:7b

ENTRYPOINT ollama serve
