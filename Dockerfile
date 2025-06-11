FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && pip install --no-cache-dir -r requirements.txt

COPY app .

EXPOSE 7860
CMD ["python", "server.py"]
