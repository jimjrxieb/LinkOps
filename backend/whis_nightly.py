"""
Whis Nightly Training System
Processes all logs from today and creates runes in the appropriate static orbs
Updated Architecture: All new runes are flagged for approval
"""

from db.database import SessionLocal
from db.models import Orb, Rune, Log
from datetime import datetime, timedelta
import uuid

def get_orb_by_agent(agent, db):
    """Get the appropriate static orb for a given agent"""
    orb_map = {
        "whis": "AI/ML Engineering Best Practices",
        "katie": "Kubernetes & CKS Best Practices",
        "igris": "DevSecOps & Platform Best Practices",
        "james": "General Ops Knowledge"
    }
    name = orb_map.get(agent.lower())
    if not name:
        # Default to James orb for unknown agents
        name = "General Ops Knowledge"
    return db.query(Orb).filter(Orb.name == name).first()

def train_whis_nightly():
    """Process all logs from today and create runes in appropriate orbs"""
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        
        # Get all logs from today
        logs = db.query(Log).filter(
            Log.created_at >= today
        ).order_by(Log.created_at.desc()).all()
        
        task_counter = {}
        runes_created = 0
        orbs_updated = set()

        for log in logs:
            # Count repeated tasks
            key = (log.agent, log.task_id)
            task_counter[key] = task_counter.get(key, 0) + 1

            # Get the appropriate orb for this agent
            orb = get_orb_by_agent(log.agent, db)
            if not orb:
                print(f"Warning: No orb found for agent {log.agent}")
                continue

            # Create content for the rune
            content = f"[{log.task_id}] {log.action}: {log.result}"
            
            # Check if we already have a similar rune to avoid duplicates
            existing_rune = db.query(Rune).filter(
                Rune.orb_id == orb.id,
                Rune.task_id == log.task_id,
                Rune.script_content.contains(log.action[:50])  # Partial match
            ).first()
            
            if existing_rune:
                # Update existing rune with new information
                existing_rune.script_content += f"\n\n--- Update {datetime.utcnow().isoformat()} ---\n{content}"
                existing_rune.version += 1
                print(f"Updated existing rune {existing_rune.id} for task {log.task_id}")
            else:
                # Create new rune - marked as flagged for approval
                rune = Rune(
                    orb_id=orb.id,
                    script_path=f"nightly_training/{log.task_id}",
                    script_content=content,
                    language="training",
                    version=1,
                    task_id=log.task_id,
                    is_flagged=True  # requires human approval
                )
                db.add(rune)
                runes_created += 1
                print(f"Created new flagged rune for task {log.task_id} in {orb.name}")

            orbs_updated.add(orb.name)

        # Commit all changes
        db.commit()
        
        # Get repeated tasks (training signal strength)
        repeated_tasks = [
            {"agent": agent, "task_id": task_id, "count": count}
            for (agent, task_id), count in task_counter.items()
            if count > 1
        ]

        return {
            "status": "trained",
            "tasks_processed": len(logs),
            "runes_created": runes_created,
            "orbs_updated": list(orbs_updated),
            "repeated_tasks": repeated_tasks,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error during nightly training: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close()

def get_training_stats():
    """Get statistics about the training system"""
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        
        # Get today's logs by agent
        logs_today = db.query(Log).filter(Log.created_at >= today).all()
        agent_counts = {}
        
        for log in logs_today:
            agent_counts[log.agent] = agent_counts.get(log.agent, 0) + 1
        
        # Get total runes by orb
        orbs = db.query(Orb).all()
        orb_stats = {}
        
        for orb in orbs:
            rune_count = db.query(Rune).filter(Rune.orb_id == orb.id).count()
            orb_stats[orb.name] = rune_count
        
        # Get approval queue stats
        pending_approvals = db.query(Rune).filter(Rune.is_flagged == True).count()
        
        return {
            "logs_today": len(logs_today),
            "agent_breakdown": agent_counts,
            "orb_rune_counts": orb_stats,
            "pending_approvals": pending_approvals,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close() 