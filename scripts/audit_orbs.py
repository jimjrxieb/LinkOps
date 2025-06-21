#!/usr/bin/env python3
"""
Audit script to detect similar orbs and suggest merges
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db.models import Orb, Rune
from core.db.database import get_db, SessionLocal
from difflib import SequenceMatcher
from typing import List, Tuple
import uuid
from core.utils.llm import infer_agent_category

def is_similar(a: str, b: str, threshold: float = 0.8) -> bool:
    """Check if two strings are similar using SequenceMatcher"""
    if not a or not b:
        return False
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def audit_similar_orbs(threshold: float = 0.8) -> List[Tuple[Orb, Orb, str]]:
    """Find similar orbs and return pairs with similarity type"""
    db = next(get_db())
    orbs = db.query(Orb).all()
    similar_pairs = []
    
    print(f"🔍 Auditing {len(orbs)} orbs for similarity (threshold: {threshold})")
    
    # Naive O(n²) comparison for demo
    for i, orb1 in enumerate(orbs):
        for orb2 in orbs[i+1:]:
            name_similar = is_similar(orb1.name, orb2.name, threshold)
            desc_similar = is_similar(orb1.description, orb2.description, threshold)
            
            if name_similar or desc_similar:
                similarity_type = []
                if name_similar:
                    similarity_type.append("name")
                if desc_similar:
                    similarity_type.append("description")
                
                similar_pairs.append((orb1, orb2, "+".join(similarity_type)))
                print(f"🔁 Similar ({'+'.join(similarity_type)}): {orb1.name} <--> {orb2.name}")
    
    db.close()
    return similar_pairs

def suggest_merges(similar_pairs: List[Tuple[Orb, Orb, str]]) -> List[dict]:
    """Generate merge suggestions for similar orbs"""
    suggestions = []
    
    for orb1, orb2, similarity_type in similar_pairs:
        suggestion = {
            "orb1_id": str(orb1.id),
            "orb1_name": orb1.name,
            "orb1_category": orb1.category,
            "orb2_id": str(orb2.id),
            "orb2_name": orb2.name,
            "orb2_category": orb2.category,
            "similarity_type": similarity_type,
            "suggestion": f"Consider merging '{orb1.name}' with '{orb2.name}' (similar {similarity_type})"
        }
        suggestions.append(suggestion)
    
    return suggestions

def audit_by_patterns() -> List[dict]:
    """Audit orbs based on common patterns"""
    db = next(get_db())
    orbs = db.query(Orb).all()
    pattern_suggestions = []
    
    patterns = {
        "pod_creation": ["create pod", "deploy pod", "kubernetes pod"],
        "model_serving": ["serve model", "model serving", "fastapi model"],
        "mlflow": ["mlflow", "mlflow tracking", "mlflow model"],
        "docker": ["docker", "container", "dockerfile"],
        "monitoring": ["prometheus", "metrics", "monitoring"]
    }
    
    for orb in orbs:
        orb_lower = orb.description.lower() if orb.description else ""
        for pattern_name, keywords in patterns.items():
            if any(keyword in orb_lower for keyword in keywords):
                pattern_suggestions.append({
                    "orb_id": str(orb.id),
                    "orb_name": orb.name,
                    "pattern": pattern_name,
                    "note": f"Consider grouping with other {pattern_name} orbs"
                })
                break
    
    db.close()
    return pattern_suggestions

def reassign_runes_to_master_orbs():
    db = SessionLocal()
    master_orbs = {}
    try:
        # Ensure master orbs exist
        for agent in ["katie", "igris", "whis", "james"]:
            orb = db.query(Orb).filter(Orb.name == agent).first()
            if not orb:
                orb = Orb(name=agent, description=f"{agent.capitalize()} agent orb", category=agent)
                db.add(orb)
                db.commit()
                db.refresh(orb)
            master_orbs[agent] = orb

        # Reassign all runes
        for rune in db.query(Rune).all():
            # Use script_content, script_path, or task_id to infer agent
            text = (rune.script_content or "") + " " + (rune.script_path or "") + " " + (getattr(rune, "task_id", "") or "")
            agent = infer_agent_category(text)
            master_orb = master_orbs[agent]
            if rune.orb_id != master_orb.id:
                print(f"Reassigning Rune {rune.id} to {agent} orb")
                rune.orb_id = master_orb.id
        db.commit()

        # Delete non-master orbs
        for orb in db.query(Orb).all():
            if orb.name not in master_orbs:
                print(f"Deleting non-master Orb {orb.id} ({orb.name})")
                db.delete(orb)
        db.commit()
        print("Cleanup complete. All runes are now under the four master orbs.")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 Starting Orb Audit...")
    print("=" * 50)
    
    # Find similar orbs
    similar_pairs = audit_similar_orbs(threshold=0.8)
    
    if similar_pairs:
        print(f"\n📋 Found {len(similar_pairs)} similar orb pairs:")
        suggestions = suggest_merges(similar_pairs)
        for suggestion in suggestions:
            print(f"  • {suggestion['suggestion']}")
    else:
        print("✅ No similar orbs found!")
    
    print("\n" + "=" * 50)
    
    # Pattern-based audit
    print("🔍 Pattern-based audit...")
    pattern_suggestions = audit_by_patterns()
    
    if pattern_suggestions:
        print(f"\n📋 Found {len(pattern_suggestions)} pattern-based suggestions:")
        for suggestion in pattern_suggestions:
            print(f"  • {suggestion['orb_name']}: {suggestion['note']}")
    else:
        print("✅ No pattern-based suggestions!")
    
    print("\n🎯 Audit complete!")
    
    reassign_runes_to_master_orbs() 