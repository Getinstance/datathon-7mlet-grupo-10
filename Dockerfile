FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY app ./app
COPY data ./data

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn numpy pandas

EXPOSE 8000 8080

CMD ["sh", "-c", "uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"]
