FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Create directory for generated services
RUN mkdir -p /app/generated_services

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"] 