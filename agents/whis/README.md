# Whis Agent Microservice

A minimal FastAPI microservice for the Whis agent.

## Endpoints
- `GET /health` — Health check
- `POST /execute` — Simulated agent execution

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

## Docker
```bash
docker build -t whis-agent .
docker run -p 8003:8003 whis-agent
``` 