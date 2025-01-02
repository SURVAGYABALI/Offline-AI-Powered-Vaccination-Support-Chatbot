FROM python:3.8.8

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama start & \
    sleep 5 && \
    ollama run meditron && \
    kill $(pgrep ollama)
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "ollama serve & uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]

