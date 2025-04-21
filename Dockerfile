FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libgomp1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry yt-dlp

COPY . .

RUN poetry config virtualenvs.create false

RUN poetry install
