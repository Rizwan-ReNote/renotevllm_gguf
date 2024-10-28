FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y sudo python3 python3-pip curl && \
    apt-get clean

RUN pip3 install fastapi uvicorn python-multipart

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip3 install ollama

COPY . /app

EXPOSE 8080

# Start the Ollama service in the background and run the FastAPI server
CMD ollama serve & \
    sleep 5 && \
    ollama run aiden_lu/minicpm-v2.6:Q4_K_M & \
    uvicorn app:app --host 0.0.0.0 --port 8080