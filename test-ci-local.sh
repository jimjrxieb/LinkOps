#!/bin/bash

echo "🧪 Testing LinkOps CI locally..."

# Test backend imports
echo "📦 Testing backend imports..."
cd backend
python3 -c "from main import app; print('✅ Backend imports successful')" || exit 1
python3 -c "from models.log import LogEntry; from models.rune import RuneCandidate; print('✅ Database models imported successfully')" || exit 1
python3 -c "from routes.data_collect import router; from routes.whis import router; print('✅ Route imports successful')" || exit 1
cd ..

# Test frontend build
echo "🎨 Testing frontend build..."
cd frontend
npm install || exit 1
npm run build || exit 1
echo "✅ Frontend build successful"
cd ..

echo "🎉 All local CI tests passed!" 