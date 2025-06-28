#!/bin/bash

echo "🧹 Tearing everything down (including volumes)..."
docker compose down -v --remove-orphans

echo "🗑️ Pruning unused Docker data (be careful!)"
docker system prune -af --volumes

echo "✅ Clean slate. You can now run ./build.sh to restart."
