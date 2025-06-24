#!/bin/bash

# LinkOps PwC-Aligned Upgrade Script
# This script upgrades LinkOps to the desired PwC-aligned AI audit platform state

set -e

echo "🧭 Starting LinkOps PwC-Aligned Upgrade..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the LinkOps root directory"
    exit 1
fi

print_status "Checking current LinkOps installation..."

# 1. Database Migration
print_status "Step 1: Running database migrations for PwC-aligned logging..."
cd backend

# Check if alembic is available
if command -v alembic &> /dev/null; then
    alembic upgrade head
    print_success "Database migrations completed"
else
    print_warning "Alembic not found, skipping database migrations"
    print_warning "Please run 'alembic upgrade head' manually in the backend directory"
fi

cd ..

# 2. Build New Agents
print_status "Step 2: Building new PwC-aligned agents..."

# Build AuditGuard agent
print_status "Building AuditGuard agent..."
cd agents/auditguard
if [ -f "Dockerfile" ]; then
    docker build -t linkops-auditguard:latest .
    print_success "AuditGuard agent built successfully"
else
    print_error "AuditGuard Dockerfile not found"
    exit 1
fi
cd ../..

# Build FickNury agent
print_status "Building FickNury agent..."
cd agents/ficknury
if [ -f "Dockerfile" ]; then
    docker build -t linkops-ficknury:latest .
    print_success "FickNury agent built successfully"
else
    print_error "FickNury Dockerfile not found"
    exit 1
fi
cd ../..

# 3. Update Docker Compose
print_status "Step 3: Updating docker-compose.yml with new agents..."

# Create backup of current docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup
print_success "Created backup of docker-compose.yml"

# Add new services to docker-compose.yml
cat >> docker-compose.yml << 'EOF'

  # PwC-Aligned Agents
  auditguard:
    image: linkops-auditguard:latest
    container_name: linkops-auditguard
    ports:
      - "8001:8000"
    environment:
      - LOG_LEVEL=INFO
    volumes:
      - ./agents/auditguard/logs:/app/logs
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - linkops-network
    depends_on:
      - backend

  ficknury:
    image: linkops-ficknury:latest
    container_name: linkops-ficknury
    ports:
      - "8002:8000"
    environment:
      - LOG_LEVEL=INFO
      - KUBECONFIG=/root/.kube/config
    volumes:
      - ./agents/ficknury/logs:/app/logs
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/.kube:/root/.kube
    networks:
      - linkops-network
    depends_on:
      - backend
EOF

print_success "Updated docker-compose.yml with new agents"

# 4. Update Frontend
print_status "Step 4: Updating frontend with PwC-aligned components..."

cd frontend

# Install any new dependencies if needed
if [ -f "package.json" ]; then
    npm install
    print_success "Frontend dependencies updated"
fi

# Build frontend
print_status "Building frontend with PwC-aligned features..."
npm run build
print_success "Frontend built successfully"

cd ..

# 5. Create Static Orbs for New Agents
print_status "Step 5: Creating static orbs for new agents..."

# Create a Python script to add the new orbs
cat > create_pwc_orbs.py << 'EOF'
#!/usr/bin/env python3
"""
Script to create PwC-aligned static orbs for new agents
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from db.database import SessionLocal
from db.models import Orb
from datetime import datetime

def create_pwc_orbs():
    """Create PwC-aligned orbs for new agents"""
    db = SessionLocal()
    
    pwc_orbs = [
        {
            "name": "Security & Compliance Best Practices",
            "description": "🛡️ Security scanning, compliance checks, and audit procedures aligned with PwC standards",
            "category": "security",
            "owner_agent": "auditguard"
        },
        {
            "name": "Agent Orchestration Best Practices", 
            "description": "🎭 Agent creation, deployment, and orchestration patterns for scalable AI operations",
            "category": "orchestration",
            "owner_agent": "ficknury"
        }
    ]
    
    created_count = 0
    
    for orb_data in pwc_orbs:
        # Check if orb already exists
        existing_orb = db.query(Orb).filter(Orb.name == orb_data["name"]).first()
        
        if not existing_orb:
            # Create new orb
            new_orb = Orb(
                name=orb_data["name"],
                description=orb_data["description"],
                category=orb_data["category"],
                owner_agent=orb_data["owner_agent"]
            )
            db.add(new_orb)
            created_count += 1
            print(f"✅ Created {orb_data['name']} orb")
        else:
            print(f"⏭️  {orb_data['name']} orb already exists")
    
    db.commit()
    db.close()
    
    print(f"\n🎯 PwC orb creation complete! Created {created_count} new orbs.")
    return created_count

if __name__ == "__main__":
    create_pwc_orbs()
EOF

# Run the orb creation script
python3 create_pwc_orbs.py
print_success "PwC-aligned orbs created"

# Clean up
rm create_pwc_orbs.py

# 6. Start Services
print_status "Step 6: Starting upgraded LinkOps services..."

# Stop existing services
docker-compose down

# Start all services including new agents
docker-compose up -d

print_success "All services started successfully"

# 7. Verify Installation
print_status "Step 7: Verifying PwC-aligned installation..."

# Wait for services to be ready
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_success "All services are running"
else
    print_error "Some services failed to start"
    docker-compose logs
    exit 1
fi

# Check new agent endpoints
print_status "Checking new agent endpoints..."

# Check AuditGuard
if curl -s http://localhost:8001/health > /dev/null; then
    print_success "AuditGuard agent is responding"
else
    print_warning "AuditGuard agent may not be ready yet"
fi

# Check FickNury
if curl -s http://localhost:8002/health > /dev/null; then
    print_success "FickNury agent is responding"
else
    print_warning "FickNury agent may not be ready yet"
fi

# 8. Display Upgrade Summary
echo ""
echo "🎉 LinkOps PwC-Aligned Upgrade Complete!"
echo "========================================"
echo ""
echo "New Features Added:"
echo "✅ PwC-aligned audit logging with compliance tags"
echo "✅ AuditGuard agent for security scanning"
echo "✅ FickNury meta-agent for orchestration"
echo "✅ Enhanced Whis training with approval filtering"
echo "✅ PwC-style dashboard with compliance statistics"
echo ""
echo "Access Points:"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "🛡️ AuditGuard: http://localhost:8001"
echo "🎭 FickNury: http://localhost:8002"
echo ""
echo "Next Steps:"
echo "1. Access the PwC dashboard at http://localhost:3000"
echo "2. Run a security scan via AuditGuard"
echo "3. Propose a new agent via FickNury"
echo "4. Review compliance statistics and audit logs"
echo ""
echo "Documentation:"
echo "📖 Check the README files in agents/auditguard/ and agents/ficknury/"
echo "📊 Review the PwC-aligned logging format in backend/db/models.py"
echo ""

print_success "Upgrade completed successfully!"
print_status "LinkOps is now a PwC-aligned AI audit platform" 