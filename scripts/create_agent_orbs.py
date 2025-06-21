#!/usr/bin/env python3
"""
Script to create one orb per agent if they don't already exist
"""

from core.db.models import Orb
from core.db.database import get_db
from datetime import datetime

def create_agent_orbs():
    """Create one orb per agent if they don't already exist"""
    db = next(get_db())
    
    agents = [
        {
            "name": "whis",
            "description": "🧠 Whis: MLOps Automation Agent - Specializes in model deployment, training pipelines, and infrastructure automation",
            "category": "agent"
        },
        {
            "name": "katie", 
            "description": "📊 Katie: Data & Analytics Agent - Handles data processing, ETL pipelines, and analytics workflows",
            "category": "agent"
        },
        {
            "name": "igris",
            "description": "🔧 Igris: Infrastructure & DevOps Agent - Manages Kubernetes, Docker, and infrastructure as code",
            "category": "agent"
        },
        {
            "name": "james",
            "description": "🔍 James: Search & Discovery Agent - Handles knowledge retrieval, documentation, and search optimization",
            "category": "agent"
        }
    ]
    
    created_count = 0
    
    for agent in agents:
        # Check if agent orb already exists
        existing_orb = db.query(Orb).filter(Orb.name == agent["name"]).first()
        
        if not existing_orb:
            # Create new agent orb
            new_orb = Orb(
                name=agent["name"],
                description=agent["description"],
                category=agent["category"]
            )
            db.add(new_orb)
            created_count += 1
            print(f"✅ Created {agent['name']} agent orb")
        else:
            print(f"⏭️  {agent['name']} agent orb already exists")
    
    db.commit()
    db.close()
    
    print(f"\n🎯 Agent orb creation complete! Created {created_count} new agent orbs.")
    return created_count

if __name__ == "__main__":
    print("🤖 Creating agent orbs...")
    create_agent_orbs() 