#!/bin/bash

echo "🛑 [ARISE] Terminating old shadows..."
docker compose down

echo "🛠️ [ARISE] Reforging containers..."
docker compose build

echo "👁️ [ARISE] Summoning LinkOps agents..."
docker compose up -d --remove-orphans

echo "🧠 [ARISE] James and the agents await your command:"
echo "→ Backend:   http://localhost:8000"
echo "→ Frontend:  http://localhost:3000"
