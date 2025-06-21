#!/bin/bash

# 🧠 LinkOps HoloCore Startup Script
# Elite AI Command Center Launcher

echo "🧠 LinkOps HoloCore - Elite AI Command Center"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists docker; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+ first.${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm not found. Please install npm first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites found${NC}"
echo ""

# Start backend
echo "🚀 Starting LinkOps Core Backend..."
cd core

if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found in core directory${NC}"
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up --build -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Backend failed to start within 30 seconds${NC}"
        exit 1
    fi
    echo -n "."
    sleep 1
done

cd ..

# Start frontend
echo ""
echo "🎨 Starting HoloCore Frontend..."

cd frontend

if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found in frontend directory${NC}"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Check if port 3000 is available
if port_in_use 3000; then
    echo -e "${YELLOW}⚠️  Port 3000 is in use. Frontend may not start properly.${NC}"
fi

echo "🌐 Starting development server..."
echo ""
echo -e "${CYAN}🎯 HoloCore URLs:${NC}"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
echo -e "${GREEN}Health Check:${NC} http://localhost:8000/health"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "• Use Ctrl+C to stop the frontend"
echo "• Use 'docker-compose down' in core/ to stop backend"
echo "• Check logs with 'docker-compose logs -f' in core/"
echo ""
echo -e "${CYAN}🚀 Starting HoloCore...${NC}"

# Start the development server
npm run dev 