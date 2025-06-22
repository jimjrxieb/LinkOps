"""
James Task Analyzer
Analyzes tasks and determines the best agent assignments based on orbs and runes.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import Orb, Rune, Task


class TaskAnalyzer:
    """James' task analysis and ranking system"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Agent keyword mappings for task classification
        self.agent_keywords = {
            "katie": {
                "primary": ["kubernetes", "k8s", "pod", "deployment", "service", "configmap", "secret", "namespace", "cluster", "node"],
                "secondary": ["cka", "cks", "certified", "container", "docker", "helm", "operator", "crd", "rbac", "network", "storage"],
                "complexity_indicators": ["multi-cluster", "high-availability", "disaster-recovery", "security-context", "resource-limits"]
            },
            "igris": {
                "primary": ["terraform", "vault", "ansible", "puppet", "chef", "infrastructure", "iac", "devops", "security", "compliance"],
                "secondary": ["aws", "azure", "gcp", "cloud", "provisioning", "automation", "ci/cd", "gitops", "monitoring", "logging"],
                "complexity_indicators": ["multi-cloud", "zero-trust", "compliance-audit", "disaster-recovery", "cost-optimization"]
            },
            "whis": {
                "primary": ["train", "ml", "ai", "model", "neural", "learning", "data", "analytics", "prediction", "classification"],
                "secondary": ["dataset", "feature", "algorithm", "accuracy", "performance", "optimization", "inference", "deployment"],
                "complexity_indicators": ["deep-learning", "reinforcement-learning", "nlp", "computer-vision", "real-time-inference"]
            },
            "james": {
                "primary": ["route", "coordinate", "manage", "organize", "plan", "schedule", "prioritize", "orchestrate"],
                "secondary": ["workflow", "pipeline", "integration", "api", "webhook", "event", "trigger", "condition"],
                "complexity_indicators": ["multi-agent", "conditional-logic", "error-handling", "retry-mechanism", "fallback"]
            }
        }
        
        # Priority indicators
        self.priority_indicators = {
            "high": ["urgent", "critical", "emergency", "immediate", "asap", "break", "down", "error", "fail", "outage"],
            "medium": ["important", "needed", "required", "should", "recommended", "update", "upgrade"],
            "low": ["nice-to-have", "optional", "future", "later", "when-convenient", "explore", "investigate"]
        }
        
        # Complexity scoring factors
        self.complexity_factors = {
            "scope": {"small": 1, "medium": 2, "large": 3},
            "dependencies": {"none": 1, "few": 2, "many": 3},
            "novelty": {"routine": 1, "standard": 2, "innovative": 3},
            "risk": {"low": 1, "medium": 2, "high": 3}
        }

    def analyze_task(self, task_input: str, task_id: Optional[str] = None) -> Dict:
        """
        Analyze a task and return comprehensive ranking and recommendations.
        
        Args:
            task_input: The task description
            task_id: Optional task identifier
            
        Returns:
            Dict containing analysis results
        """
        task_input_lower = task_input.lower()
        
        # 1. Agent scoring and ranking
        agent_scores = self._calculate_agent_scores(task_input_lower)
        
        # 2. Priority assessment
        priority = self._assess_priority(task_input_lower)
        
        # 3. Complexity assessment
        complexity = self._assess_complexity(task_input_lower)
        
        # 4. Find matching orbs and runes
        matching_orbs = self._find_matching_orbs(task_input_lower)
        matching_runes = self._find_matching_runes(task_input_lower)
        
        # 5. Calculate urgency score
        urgency_score = self._calculate_urgency(priority, complexity)
        
        # 6. Determine recommended agent
        recommended_agent = max(agent_scores, key=agent_scores.get)
        
        # 7. Generate task insights
        insights = self._generate_insights(task_input_lower, agent_scores, matching_orbs, matching_runes)
        
        return {
            "task_id": task_id,
            "task_input": task_input,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "agent_scores": agent_scores,
            "recommended_agent": recommended_agent,
            "priority": priority,
            "complexity": complexity,
            "urgency_score": urgency_score,
            "matching_orbs": matching_orbs,
            "matching_runes": matching_runes,
            "insights": insights,
            "confidence_score": self._calculate_confidence(agent_scores, matching_orbs, matching_runes)
        }

    def _calculate_agent_scores(self, task_input: str) -> Dict[str, int]:
        """Calculate confidence scores for each agent based on keywords"""
        scores = {agent: 10 for agent in self.agent_keywords.keys()}
        
        for agent, keywords in self.agent_keywords.items():
            # Primary keywords (higher weight)
            for keyword in keywords["primary"]:
                if keyword in task_input:
                    scores[agent] += 25
            
            # Secondary keywords (medium weight)
            for keyword in keywords["secondary"]:
                if keyword in task_input:
                    scores[agent] += 15
            
            # Complexity indicators (bonus for specialized tasks)
            for indicator in keywords["complexity_indicators"]:
                if indicator in task_input:
                    scores[agent] += 10
        
        return scores

    def _assess_priority(self, task_input: str) -> str:
        """Assess task priority based on urgency indicators"""
        urgency_count = 0
        importance_count = 0
        
        for indicator in self.priority_indicators["high"]:
            if indicator in task_input:
                urgency_count += 2
        
        for indicator in self.priority_indicators["medium"]:
            if indicator in task_input:
                importance_count += 1
        
        if urgency_count >= 2:
            return "high"
        elif importance_count >= 2 or urgency_count >= 1:
            return "medium"
        else:
            return "low"

    def _assess_complexity(self, task_input: str) -> Dict:
        """Assess task complexity based on various factors"""
        complexity_score = 0
        factors = {}
        
        # Scope assessment
        if any(word in task_input for word in ["simple", "basic", "quick", "single"]):
            factors["scope"] = "small"
            complexity_score += 1
        elif any(word in task_input for word in ["comprehensive", "full", "complete", "end-to-end"]):
            factors["scope"] = "large"
            complexity_score += 3
        else:
            factors["scope"] = "medium"
            complexity_score += 2
        
        # Dependencies assessment
        if any(word in task_input for word in ["dependencies", "prerequisites", "requirements", "setup", "configuration"]):
            factors["dependencies"] = "many"
            complexity_score += 3
        elif any(word in task_input for word in ["standalone", "independent", "self-contained"]):
            factors["dependencies"] = "none"
            complexity_score += 1
        else:
            factors["dependencies"] = "few"
            complexity_score += 2
        
        # Novelty assessment
        if any(word in task_input for word in ["new", "innovative", "experimental", "research", "prototype"]):
            factors["novelty"] = "innovative"
            complexity_score += 3
        elif any(word in task_input for word in ["routine", "standard", "template", "boilerplate"]):
            factors["novelty"] = "routine"
            complexity_score += 1
        else:
            factors["novelty"] = "standard"
            complexity_score += 2
        
        # Risk assessment
        if any(word in task_input for word in ["production", "critical", "security", "compliance", "audit"]):
            factors["risk"] = "high"
            complexity_score += 3
        elif any(word in task_input for word in ["development", "testing", "sandbox", "demo"]):
            factors["risk"] = "low"
            complexity_score += 1
        else:
            factors["risk"] = "medium"
            complexity_score += 2
        
        # Overall complexity level
        if complexity_score <= 6:
            overall = "low"
        elif complexity_score <= 10:
            overall = "medium"
        else:
            overall = "high"
        
        return {
            "overall": overall,
            "score": complexity_score,
            "factors": factors
        }

    def _find_matching_orbs(self, task_input: str) -> List[Dict]:
        """Find orbs that match the task requirements"""
        matching_orbs = []
        
        # Get all orbs from database
        orbs = self.db.query(Orb).all()
        
        for orb in orbs:
            match_score = 0
            
            # Check orb name
            if orb.name.lower() in task_input:
                match_score += 30
            
            # Check orb description
            if orb.description and orb.description.lower() in task_input:
                match_score += 20
            
            # Check orb category
            if orb.category and orb.category.lower() in task_input:
                match_score += 15
            
            # Check for keyword matches in description
            if orb.description:
                desc_lower = orb.description.lower()
                for agent, keywords in self.agent_keywords.items():
                    for keyword in keywords["primary"]:
                        if keyword in desc_lower:
                            match_score += 10
            
            if match_score > 0:
                matching_orbs.append({
                    "id": str(orb.id),
                    "name": orb.name,
                    "description": orb.description,
                    "category": orb.category,
                    "match_score": match_score
                })
        
        # Sort by match score
        matching_orbs.sort(key=lambda x: x["match_score"], reverse=True)
        return matching_orbs[:5]  # Return top 5 matches

    def _find_matching_runes(self, task_input: str) -> List[Dict]:
        """Find runes that match the task requirements"""
        matching_runes = []
        
        # Get all runes from database
        runes = self.db.query(Rune).all()
        
        for rune in runes:
            match_score = 0
            
            # Check rune language
            if rune.language.lower() in task_input:
                match_score += 25
            
            # Check script content
            if rune.script_content and rune.script_content.lower() in task_input:
                match_score += 20
            
            # Check script path
            if rune.script_path and rune.script_path.lower() in task_input:
                match_score += 15
            
            # Check for keyword matches in content
            if rune.script_content:
                content_lower = rune.script_content.lower()
                for agent, keywords in self.agent_keywords.items():
                    for keyword in keywords["primary"]:
                        if keyword in content_lower:
                            match_score += 10
            
            if match_score > 0:
                matching_runes.append({
                    "id": str(rune.id),
                    "orb_id": str(rune.orb_id),
                    "language": rune.language,
                    "script_path": rune.script_path,
                    "version": rune.version,
                    "match_score": match_score
                })
        
        # Sort by match score
        matching_runes.sort(key=lambda x: x["match_score"], reverse=True)
        return matching_runes[:5]  # Return top 5 matches

    def _calculate_urgency(self, priority: str, complexity: Dict) -> float:
        """Calculate urgency score based on priority and complexity"""
        priority_scores = {"low": 1.0, "medium": 2.0, "high": 3.0}
        complexity_scores = {"low": 1.0, "medium": 1.5, "high": 2.0}
        
        priority_score = priority_scores.get(priority, 1.0)
        complexity_score = complexity_scores.get(complexity["overall"], 1.0)
        
        # Urgency is higher for high priority and lower complexity (easier to complete quickly)
        return priority_score * (1.0 / complexity_score)

    def _generate_insights(self, task_input: str, agent_scores: Dict, matching_orbs: List, matching_runes: List) -> List[str]:
        """Generate insights about the task"""
        insights = []
        
        # Agent insights
        top_agent = max(agent_scores, key=agent_scores.get)
        top_score = agent_scores[top_agent]
        
        if top_score >= 80:
            insights.append(f"Strong match for {top_agent} agent (score: {top_score})")
        elif top_score >= 50:
            insights.append(f"Good match for {top_agent} agent (score: {top_score})")
        else:
            insights.append(f"Weak agent matches - may need manual assignment")
        
        # Orb insights
        if matching_orbs:
            insights.append(f"Found {len(matching_orbs)} relevant orbs for reference")
        
        # Rune insights
        if matching_runes:
            insights.append(f"Found {len(matching_runes)} relevant runes for implementation")
        
        # Complexity insights
        if "kubernetes" in task_input and "production" in task_input:
            insights.append("Production Kubernetes task - consider security and compliance requirements")
        
        if "terraform" in task_input and "multi-cloud" in task_input:
            insights.append("Multi-cloud Terraform task - consider state management and provider configuration")
        
        return insights

    def _calculate_confidence(self, agent_scores: Dict, matching_orbs: List, matching_runes: List) -> float:
        """Calculate confidence score for the analysis"""
        max_score = max(agent_scores.values())
        orb_bonus = min(len(matching_orbs) * 0.1, 0.5)  # Max 0.5 bonus for orbs
        rune_bonus = min(len(matching_runes) * 0.1, 0.5)  # Max 0.5 bonus for runes
        
        # Normalize agent score to 0-1 range (assuming max possible score is around 100)
        agent_confidence = min(max_score / 100.0, 1.0)
        
        return min(agent_confidence + orb_bonus + rune_bonus, 1.0)

    def store_analysis(self, task_id: str, analysis: Dict) -> bool:
        """Store the analysis results in the database"""
        try:
            # Update the task with analysis results
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if task:
                # Store analysis as JSON in a new field or as part of agent_rankings
                analysis_json = json.dumps(analysis)
                # For now, we'll store it in agent_rankings field (we can add a dedicated field later)
                task.agent_rankings = analysis_json
                self.db.commit()
                return True
        except Exception as e:
            print(f"Error storing analysis: {e}")
            return False
        
        return False


def analyze_task(task_input: str, db: Session, task_id: Optional[str] = None) -> Dict:
    """
    Convenience function to analyze a task.
    
    Args:
        task_input: The task description
        db: Database session
        task_id: Optional task identifier
        
    Returns:
        Dict containing analysis results
    """
    analyzer = TaskAnalyzer(db)
    analysis = analyzer.analyze_task(task_input, task_id)
    
    # Store analysis if task_id is provided
    if task_id:
        analyzer.store_analysis(task_id, analysis)
    
    return analysis 