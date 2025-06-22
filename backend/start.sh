#!/bin/bash

echo "🚀 Starting LinkOps James Workflow Backend..."

# Check if we're in a container
if [ -f /.dockerenv ]; then
    echo "📦 Running in Docker container"
else
    echo "🖥️  Running in local environment"
fi

# Wait for dependencies if needed
echo "⏳ Checking dependencies..."

# Start the application
echo "🌐 Starting FastAPI server..."
exec python3 main.py 