"""
Task processor logic for LinkOps
Analyzes tasks and matches them to appropriate agents using orbs and runes.
"""

from typing import Dict, Any, List, Optional
import re
import json

class TaskProcessor:
    """Main task processor that analyzes and ranks tasks"""
    
    def __init__(self):
        # Agent keywords and their specialties
        self.agent_keywords = {
            "katie": {
                "keywords": [
                    "kubernetes", "k8s", "pod", "deployment", "service", "namespace",
                    "helm", "docker", "container", "infrastructure", "terraform",
                    "aws", "gcp", "azure", "cloud", "cluster", "node", "ingress",
                    "configmap", "secret", "persistentvolume", "pvc", "job", "cronjob"
                ],
                "specialties": ["Infrastructure", "DevOps", "Cloud", "Container Orchestration"],
                "confidence_boost": 1.0
            },
            "igris": {
                "keywords": [
                    "ai", "ml", "machine learning", "neural network", "model",
                    "training", "inference", "data science", "pandas", "numpy",
                    "tensorflow", "pytorch", "scikit-learn", "jupyter", "notebook",
                    "algorithm", "prediction", "classification", "regression",
                    "deep learning", "nlp", "computer vision", "reinforcement learning"
                ],
                "specialties": ["Artificial Intelligence", "Machine Learning", "Data Science"],
                "confidence_boost": 1.0
            },
            "whis": {
                "keywords": [
                    "knowledge", "training", "learning", "documentation", "guide",
                    "tutorial", "best practice", "workflow", "process", "automation",
                    "orchestration", "integration", "api", "microservice", "architecture",
                    "design pattern", "refactoring", "optimization", "performance"
                ],
                "specialties": ["Knowledge Management", "Process Automation", "System Design"],
                "confidence_boost": 0.8
            },
            "james": {
                "keywords": [
                    "general", "help", "question", "how to", "what is", "explain",
                    "monitoring", "logging", "alerting", "dashboard", "metrics",
                    "analysis", "troubleshooting", "debugging", "support", "maintenance"
                ],
                "specialties": ["General Support", "Monitoring", "Troubleshooting"],
                "confidence_boost": 0.6
            }
        }
    
    def analyze_task(self, task_input: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a task and return agent rankings, orbs, and runes
        
        Args:
            task_input: The task description or question
            task_id: Optional task ID for tracking
            
        Returns:
            Dictionary with analysis results
        """
        # Normalize input
        task_lower = task_input.lower()
        
        # Calculate agent scores
        agent_scores = self._calculate_agent_scores(task_lower)
        
        # Get top agent
        top_agent = max(agent_scores.items(), key=lambda x: x[1])[0]
        
        # Get matching orbs and runes
        matching_orbs = self._find_matching_orbs(task_lower, top_agent)
        matching_runes = self._find_matching_runes(task_lower, top_agent)
        
        # Calculate priority and complexity
        priority = self._calculate_priority(task_lower)
        complexity_score = self._calculate_complexity(task_lower)
        
        # Generate insights
        insights = self._generate_insights(task_lower, top_agent, priority, complexity_score)
        
        return {
            "task_id": task_id,
            "task_input": task_input,
            "agent_rankings": agent_scores,
            "recommended_agent": top_agent,
            "confidence_score": agent_scores[top_agent] / 100.0,
            "matching_orbs": matching_orbs,
            "matching_runes": matching_runes,
            "priority": priority,
            "complexity_score": complexity_score,
            "insights": insights,
            "status": "analyzed"
        }
    
    def _calculate_agent_scores(self, task_lower: str) -> Dict[str, float]:
        """Calculate scores for each agent based on keyword matches"""
        scores = {agent: 0.0 for agent in self.agent_keywords.keys()}
        
        for agent, config in self.agent_keywords.items():
            for keyword in config["keywords"]:
                if keyword in task_lower:
                    # Score based on keyword importance and frequency
                    frequency = task_lower.count(keyword)
                    scores[agent] += frequency * 10 * config["confidence_boost"]
            
            # Bonus for multiple keyword matches
            matches = sum(1 for keyword in config["keywords"] if keyword in task_lower)
            if matches > 1:
                scores[agent] += matches * 5
        
        # Normalize scores to 0-100 range
        max_score = max(scores.values()) if scores.values() else 1
        if max_score > 0:
            scores = {agent: (score / max_score) * 100 for agent, score in scores.items()}
        
        return scores
    
    def _find_matching_orbs(self, task_lower: str, agent: str) -> List[Dict[str, Any]]:
        """Find matching orbs for the task and agent"""
        # This would typically query the database for orbs
        # For now, return dummy orbs based on agent
        dummy_orbs = {
            "katie": [
                {
                    "id": "k8s-orb-1",
                    "name": "Kubernetes Deployment Guide",
                    "description": "Complete guide to Kubernetes deployments and management",
                    "category": "infrastructure",
                    "owner_agent": "katie"
                },
                {
                    "id": "terraform-orb-1", 
                    "name": "Terraform Infrastructure",
                    "description": "Infrastructure as code with Terraform",
                    "category": "iac",
                    "owner_agent": "katie"
                }
            ],
            "igris": [
                {
                    "id": "ml-orb-1",
                    "name": "Machine Learning Pipeline",
                    "description": "End-to-end ML pipeline implementation",
                    "category": "ai",
                    "owner_agent": "igris"
                },
                {
                    "id": "data-orb-1",
                    "name": "Data Science Workflow",
                    "description": "Data preprocessing and analysis workflows",
                    "category": "data",
                    "owner_agent": "igris"
                }
            ],
            "whis": [
                {
                    "id": "knowledge-orb-1",
                    "name": "Knowledge Management System",
                    "description": "System for organizing and retrieving knowledge",
                    "category": "knowledge",
                    "owner_agent": "whis"
                },
                {
                    "id": "automation-orb-1",
                    "name": "Process Automation",
                    "description": "Automating repetitive tasks and workflows",
                    "category": "automation",
                    "owner_agent": "whis"
                }
            ],
            "james": [
                {
                    "id": "general-orb-1",
                    "name": "General Support Guide",
                    "description": "General troubleshooting and support procedures",
                    "category": "support",
                    "owner_agent": "james"
                },
                {
                    "id": "monitoring-orb-1",
                    "name": "System Monitoring",
                    "description": "Monitoring and alerting best practices",
                    "category": "monitoring",
                    "owner_agent": "james"
                }
            ]
        }
        
        return dummy_orbs.get(agent, [])
    
    def _find_matching_runes(self, task_lower: str, agent: str) -> List[Dict[str, Any]]:
        """Find matching runes for the task and agent"""
        # This would typically query the database for runes
        # For now, return dummy runes based on agent
        dummy_runes = {
            "katie": [
                {
                    "id": "k8s-rune-1",
                    "language": "yaml",
                    "script_path": "/scripts/k8s/deployment.yaml",
                    "script_content": "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: app-deployment\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: myapp",
                    "owner_agent": "katie"
                },
                {
                    "id": "terraform-rune-1",
                    "language": "hcl",
                    "script_path": "/scripts/terraform/main.tf",
                    "script_content": 'resource "aws_instance" "example" {\n  ami           = "ami-123456"\n  instance_type = "t2.micro"\n}',
                    "owner_agent": "katie"
                }
            ],
            "igris": [
                {
                    "id": "ml-rune-1",
                    "language": "python",
                    "script_path": "/scripts/ml/train_model.py",
                    "script_content": "import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\n\n# Load data\ndata = pd.read_csv('data.csv')\nX = data.drop('target', axis=1)\ny = data['target']\n\n# Train model\nmodel = RandomForestClassifier()\nmodel.fit(X, y)",
                    "owner_agent": "igris"
                }
            ],
            "whis": [
                {
                    "id": "knowledge-rune-1",
                    "language": "python",
                    "script_path": "/scripts/knowledge/process_docs.py",
                    "script_content": "import os\nfrom pathlib import Path\n\ndef process_documents(directory):\n    docs = []\n    for file in Path(directory).glob('**/*.md'):\n        with open(file, 'r') as f:\n            docs.append(f.read())\n    return docs",
                    "owner_agent": "whis"
                }
            ],
            "james": [
                {
                    "id": "general-rune-1",
                    "language": "bash",
                    "script_path": "/scripts/general/troubleshoot.sh",
                    "script_content": "#!/bin/bash\n\necho 'Checking system status...'\nps aux | grep -v grep\necho 'Checking disk space...'\ndf -h",
                    "owner_agent": "james"
                }
            ]
        }
        
        return dummy_runes.get(agent, [])
    
    def _calculate_priority(self, task_lower: str) -> str:
        """Calculate task priority based on keywords"""
        high_priority_keywords = ["urgent", "critical", "emergency", "broken", "down", "failed"]
        low_priority_keywords = ["nice to have", "future", "someday", "optional"]
        
        for keyword in high_priority_keywords:
            if keyword in task_lower:
                return "high"
        
        for keyword in low_priority_keywords:
            if keyword in task_lower:
                return "low"
        
        return "medium"
    
    def _calculate_complexity(self, task_lower: str) -> float:
        """Calculate task complexity score (0.0 to 1.0)"""
        complexity_indicators = [
            "complex", "complicated", "difficult", "challenging", "advanced",
            "multiple", "several", "many", "various", "different",
            "integration", "migration", "refactoring", "redesign", "architecture"
        ]
        
        complexity_score = 0.5  # Base complexity
        
        for indicator in complexity_indicators:
            if indicator in task_lower:
                complexity_score += 0.1
        
        # Cap at 1.0
        return min(complexity_score, 1.0)
    
    def _generate_insights(self, task_lower: str, top_agent: str, priority: str, complexity: float) -> List[str]:
        """Generate insights about the task"""
        insights = []
        
        # Agent-specific insights
        if top_agent == "katie":
            insights.append("This task involves infrastructure or container management")
            if "kubernetes" in task_lower:
                insights.append("Kubernetes-specific knowledge required")
        elif top_agent == "igris":
            insights.append("This task involves AI/ML or data science")
            if "training" in task_lower:
                insights.append("Model training or data processing involved")
        elif top_agent == "whis":
            insights.append("This task involves knowledge management or automation")
        else:
            insights.append("General support or monitoring task")
        
        # Priority insights
        if priority == "high":
            insights.append("High priority task - consider immediate attention")
        elif priority == "low":
            insights.append("Low priority task - can be scheduled for later")
        
        # Complexity insights
        if complexity > 0.7:
            insights.append("High complexity task - may require multiple steps")
        elif complexity < 0.3:
            insights.append("Simple task - should be quick to complete")
        
        return insights

# Global instance
task_processor = TaskProcessor()

def analyze_task(task_input: str, task_id: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to analyze a task"""
    return task_processor.analyze_task(task_input, task_id) 