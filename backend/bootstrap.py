"""
Bootstrap functionality for LinkOps Core
Creates static orbs and initializes the system
"""

from db.models import Orb
from db.database import SessionLocal
from datetime import datetime

def ensure_static_orbs():
    """Create static orbs if they don't exist"""
    db = SessionLocal()
    try:
        orbs = [
            {
                "name": "AI/ML Engineering Best Practices", 
                "category": "ai", 
                "description": "Knowledge base for Whis - MLOps, model training, ML pipelines, and AI/ML best practices"
            },
            {
                "name": "Kubernetes & CKS Best Practices", 
                "category": "kubernetes", 
                "description": "Knowledge base for Katie - Kubernetes, CKS, pod management, deployments, and container orchestration"
            },
            {
                "name": "DevSecOps & Platform Best Practices", 
                "category": "platform", 
                "description": "Knowledge base for Igris - DevOps, CI/CD, infrastructure as code, security, and platform engineering"
            },
            {
                "name": "General Ops Knowledge", 
                "category": "general", 
                "description": "Knowledge base for James - General operations, documentation, search, and discovery"
            },
        ]
        
        for orb_data in orbs:
            exists = db.query(Orb).filter(Orb.name == orb_data["name"]).first()
            if not exists:
                orb = Orb(
                    name=orb_data["name"],
                    category=orb_data["category"],
                    description=orb_data["description"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(orb)
                print(f"Created static orb: {orb_data['name']}")
            else:
                print(f"Static orb already exists: {orb_data['name']}")
        
        db.commit()
        print("Static orbs bootstrap completed")
        
    except Exception as e:
        print(f"Error during bootstrap: {e}")
        db.rollback()
    finally:
        db.close()

def get_agent_orb(agent_name: str, db_session=None):
    """Get the appropriate orb for a given agent"""
    if db_session is None:
        db_session = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        agent_orb_mapping = {
            "whis": "AI/ML Engineering Best Practices",
            "katie": "Kubernetes & CKS Best Practices", 
            "igris": "DevSecOps & Platform Best Practices",
            "james": "General Ops Knowledge"
        }
        
        orb_name = agent_orb_mapping.get(agent_name.lower())
        if not orb_name:
            # Default to James orb for unknown agents
            orb_name = "General Ops Knowledge"
        
        orb = db_session.query(Orb).filter(Orb.name == orb_name).first()
        return orb
        
    finally:
        if should_close:
            db_session.close() 