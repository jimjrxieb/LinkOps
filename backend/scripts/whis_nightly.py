#!/usr/bin/env python3
"""
Whis Nightly Training Script
Processes pending queue items and marks them as trained with suggestions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db.models import WhisQueue, Rune, Orb
from core.db.database import SessionLocal
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/whis_nightly.log'),
        logging.StreamHandler()
    ]
)

def infer_category(text: str) -> str:
    """Infer category from text content"""
    text_lower = text.lower()
    
    # Katie: Kubernetes, infrastructure, platform engineering
    if any(k in text_lower for k in ["pod", "deployment", "k8s", "kubernetes", "service", "configmap", "secret", "ingress", "namespace"]):
        return "katie"
    
    # Whis: MLOps, model training, ML pipelines
    elif any(k in text_lower for k in ["mlflow", "train", "model", "pipeline", "ml", "machine learning", "prediction", "inference", "serving"]):
        return "whis"
    
    # Igris: DevOps, CI/CD, infrastructure as code
    elif any(k in text_lower for k in ["terraform", "cicd", "jenkins", "devsecops", "gitlab", "github actions", "docker", "helm", "ansible"]):
        return "igris"
    
    # James: Search, discovery, documentation, general knowledge
    else:
        return "james"

def generate_suggestion(raw_text: str, category: str) -> str:
    """Generate a suggested rune based on the raw text and category"""
    if category == "katie":
        return f"""# Kubernetes YAML Template
apiVersion: v1
kind: Pod
metadata:
  name: {raw_text.split()[0] if raw_text.split() else 'example'}-pod
spec:
  containers:
  - name: {raw_text.split()[0] if raw_text.split() else 'app'}
    image: nginx:latest
    ports:
    - containerPort: 80

# Based on input: {raw_text[:100]}..."""
    
    elif category == "whis":
        return f"""# MLOps Pipeline Template
from mlflow import log_metric, log_param
import mlflow

def train_model():
    # Training logic here
    mlflow.log_param("model_type", "random_forest")
    mlflow.log_metric("accuracy", 0.95)
    
# Based on input: {raw_text[:100]}..."""
    
    elif category == "igris":
        return f"""# DevOps Pipeline Template
stages:
  - build
  - test
  - deploy

build:
  script:
    - echo "Building application"
    - docker build -t app .

# Based on input: {raw_text[:100]}..."""
    
    else:  # james
        return f"""# Documentation Template
# {raw_text.split()[0] if raw_text.split() else 'Task'} Documentation

## Overview
{raw_text[:200]}...

## Steps
1. Step one
2. Step two
3. Step three

## Notes
- Add any additional notes here
- Based on input: {raw_text[:100]}..."""

def nightly_train():
    """Main nightly training function with enhanced source handling"""
    db = SessionLocal()
    
    try:
        # Get all pending items
        pending_items = db.query(WhisQueue).filter(WhisQueue.status == "pending").all()
        
        if not pending_items:
            logging.info("No pending items to train")
            return
        
        logging.info(f"Starting nightly training on {len(pending_items)} items")
        
        # Group items by source for different training approaches
        openai_fallbacks = [item for item in pending_items if item.source == "openai_fallback"]
        match_usages = [item for item in pending_items if item.source == "match_usage"]
        other_sources = [item for item in pending_items if item.source not in ["openai_fallback", "match_usage"]]
        
        logging.info(f"Training breakdown: {len(openai_fallbacks)} fallbacks, {len(match_usages)} match usages, {len(other_sources)} other")
        
        for item in pending_items:
            try:
                # Infer category
                category = infer_category(item.raw_text)
                
                # Generate suggestion based on source type
                if item.source == "openai_fallback":
                    # New data - create more detailed suggestions
                    suggestion = generate_fallback_suggestion(item.raw_text, category, item.task_id)
                elif item.source == "match_usage":
                    # Reinforce existing patterns
                    suggestion = generate_reinforcement_suggestion(item.raw_text, category, item.task_id)
                else:
                    # Default suggestion
                    suggestion = generate_suggestion(item.raw_text, category)
                
                # Mark as trained with source-specific suggestion
                item.status = "trained"
                item.raw_text += f"\n\n# Whis Nightly Training ({item.source}) - {datetime.now().strftime('%Y-%m-%d %H:%M')}:\n{suggestion}"
                
                logging.info(f"Trained item {item.id} ({item.task_id}) -> {category} (source: {item.source})")
                
            except Exception as e:
                logging.error(f"Error training item {item.id}: {str(e)}")
                # Mark as trained anyway to avoid infinite retries
                item.status = "trained"
                item.raw_text += f"\n\n# Training Error: {str(e)}"
        
        # Commit all changes
        db.commit()
        logging.info(f"Successfully trained {len(pending_items)} items")
        
    except Exception as e:
        logging.error(f"Error in nightly training: {str(e)}")
        db.rollback()
    finally:
        db.close()

def generate_fallback_suggestion(raw_text: str, category: str, task_id: str) -> str:
    """Generate detailed suggestion for OpenAI fallback data"""
    if category == "katie":
        return f"""# Kubernetes YAML Template (from OpenAI fallback)
# Task: {task_id}
apiVersion: v1
kind: Pod
metadata:
  name: {task_id.replace('/', '-')}-pod
  labels:
    app: {task_id.split('/')[0] if '/' in task_id else 'app'}
spec:
  containers:
  - name: {task_id.split('/')[0] if '/' in task_id else 'container'}
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"

# Based on OpenAI analysis: {raw_text[:100]}...
# This is new data that Whis should learn from."""
    
    elif category == "whis":
        return f"""# MLOps Pipeline Template (from OpenAI fallback)
# Task: {task_id}
from mlflow import log_metric, log_param, log_artifact
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model():
    # Load data
    data = pd.read_csv("data.csv")
    
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(data.drop('target', axis=1), data['target'])
    
    # Log metrics
    mlflow.log_param("model_type", "random_forest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", model.score(data.drop('target', axis=1), data['target']))
    
    return model

# Based on OpenAI analysis: {raw_text[:100]}...
# This is new data that Whis should learn from."""
    
    else:  # james or other
        return f"""# Documentation Template (from OpenAI fallback)
# Task: {task_id}

## Overview
{raw_text[:200]}...

## Implementation Steps
1. Analyze the task requirements
2. Identify the appropriate tools and frameworks
3. Create the solution
4. Test and validate
5. Document the process

## Notes
- This is new data from OpenAI fallback
- Whis should learn from this pattern
- Consider creating a new rune for similar tasks

# Based on OpenAI analysis: {raw_text[:100]}..."""

def generate_reinforcement_suggestion(raw_text: str, category: str, task_id: str) -> str:
    """Generate reinforcement suggestion for match usage data"""
    return f"""# Reinforcement Learning (from match usage)
# Task: {task_id}

## Pattern Reinforcement
This task was successfully matched to an existing rune, indicating a good pattern.

## Best Practices
- This pattern works well for {category} tasks
- Consider expanding similar runes
- Monitor usage patterns for optimization

## Suggested Improvements
- Add more examples to this pattern
- Consider creating variations
- Document common use cases

# Original content: {raw_text[:100]}...
# This reinforces existing knowledge."""

def get_training_stats():
    """Get statistics about the training queue"""
    db = SessionLocal()
    
    try:
        pending = db.query(WhisQueue).filter(WhisQueue.status == "pending").count()
        trained = db.query(WhisQueue).filter(WhisQueue.status == "trained").count()
        approved = db.query(WhisQueue).filter(WhisQueue.status == "approved").count()
        total = db.query(WhisQueue).count()
        
        logging.info(f"Queue Stats - Pending: {pending}, Trained: {trained}, Approved: {approved}, Total: {total}")
        
        return {
            "pending": pending,
            "trained": trained,
            "approved": approved,
            "total": total
        }
        
    except Exception as e:
        logging.error(f"Error getting stats: {str(e)}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Whis Nightly Training Script")
    parser.add_argument("--stats", action="store_true", help="Show training queue statistics")
    parser.add_argument("--train", action="store_true", help="Run nightly training")
    
    args = parser.parse_args()
    
    if args.stats:
        get_training_stats()
    elif args.train:
        nightly_train()
    else:
        # Default: run training
        nightly_train() 