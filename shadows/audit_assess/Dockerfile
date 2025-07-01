FROM python:3.10-slim

WORKDIR /app

# Install git for repository cloning
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic gitpython

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"] 