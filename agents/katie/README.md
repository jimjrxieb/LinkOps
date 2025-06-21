# Katie Agent Microservice

A minimal FastAPI microservice for the Katie agent.

## Endpoints
- `GET /health` — Health check
- `POST /execute` — Simulated agent execution

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Docker
```bash
docker build -t katie-agent .
docker run -p 8001:8001 katie-agent
``` 