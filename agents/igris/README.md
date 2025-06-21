# Igris Agent Microservice

A minimal FastAPI microservice for the Igris agent.

## Endpoints
- `GET /health` — Health check
- `POST /execute` — Simulated agent execution

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

## Docker
```bash
docker build -t igris-agent .
docker run -p 8002:8002 igris-agent
``` 