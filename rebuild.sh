#!/bin/bash

echo "🔁 Stopping containers..."
docker-compose down --remove-orphans

echo "🧼 Pruning unused Docker resources..."
docker system prune -f

echo "♻️ Rebuilding all containers..."
docker-compose up --build -d

echo "✅ Done! Containers rebuilt and running:"
docker ps

