"""
FickNury Evaluator - Task Scorer
Evaluates tasks against logic source capabilities and selects appropriate agents
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TaskScorer:
    """Scores tasks against logic source capabilities"""

    def __init__(self, base_path: str = "/app"):
        self.base_path = Path(base_path)
        self.logic_sources = {
            "igris_logic": {
                "name": "Igris Logic",
                "description": "Platform Engineering logic source",
                "capabilities": [
                    "infrastructure_analysis",
                    "security_assessment",
                    "platform_engineering",
                    "opendevin_integration",
                ],
                "endpoint": "http://igris_logic:8009",
                "health_endpoint": "/health",
            },
            "katie_logic": {
                "name": "Katie Logic",
                "description": "Kubernetes operations logic source",
                "capabilities": [
                    "kubernetes_operations",
                    "cluster_management",
                    "resource_scaling",
                    "log_analysis",
                    "k8gpt_integration",
                ],
                "endpoint": "http://katie_logic:8008",
                "health_endpoint": "/health",
            },
            "james_logic": {
                "name": "James Logic",
                "description": "AI assistant logic source",
                "capabilities": [
                    "voice_interaction",
                    "image_description",
                    "task_management",
                    "executive_assistance",
                ],
                "endpoint": "http://james_logic:8006",
                "health_endpoint": "/health",
            },
            "whis_logic": {
                "name": "Whis Logic",
                "description": "ML training and enhancement logic source",
                "capabilities": [
                    "orb_generation",
                    "rune_creation",
                    "agent_enhancement",
                    "training_management",
                ],
                "endpoint": "http://whis_logic:8003",
                "health_endpoint": "/health",
            },
        }

    def score_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a task against all logic sources

        Args:
            task: Task definition with requirements and parameters

        Returns:
            Scoring results with logic source rankings
        """
        try:
            logger.info(f"Scoring task: {task.get('task_id', 'unknown')}")

            task_requirements = task.get("requirements", [])
            task_type = task.get("type", "general")
            task_priority = task.get("priority", "medium")

            scores = {}

            for logic_source, config in self.logic_sources.items():
                # Calculate capability match score
                capability_score = self._calculate_capability_score(
                    task_requirements, config["capabilities"]
                )

                # Calculate type match score
                type_score = self._calculate_type_score(task_type, logic_source)

                # Calculate priority score
                priority_score = self._calculate_priority_score(
                    task_priority, logic_source
                )

                # Calculate availability score
                availability_score = self._check_logic_source_availability(config)

                # Calculate total score
                total_score = (
                    capability_score * 0.4
                    + type_score * 0.3
                    + priority_score * 0.2
                    + availability_score * 0.1
                )

                scores[logic_source] = {
                    "logic_source": logic_source,
                    "name": config["name"],
                    "description": config["description"],
                    "capability_score": capability_score,
                    "type_score": type_score,
                    "priority_score": priority_score,
                    "availability_score": availability_score,
                    "total_score": total_score,
                    "capabilities": config["capabilities"],
                    "endpoint": config["endpoint"],
                }

            # Sort by total score
            sorted_scores = sorted(
                scores.values(), key=lambda x: x["total_score"], reverse=True
            )

            # Determine if any logic source is suitable
            suitable_sources = [s for s in sorted_scores if s["total_score"] >= 0.6]

            result = {
                "task_id": task.get("task_id"),
                "task_type": task_type,
                "task_priority": task_priority,
                "scores": sorted_scores,
                "best_logic_source": sorted_scores[0] if sorted_scores else None,
                "suitable_sources": suitable_sources,
                "recommendation": self._generate_recommendation(sorted_scores, task),
                "scored_at": "{{datetime.now().isoformat()}}",
            }

            logger.info(
                f"Task scoring complete. Best: "
                f"{result['best_logic_source']['logic_source'] if result['best_logic_source'] else 'None'}"
            )
            return result

        except Exception as e:
            logger.error(f"Task scoring failed: {str(e)}")
            return {"error": str(e), "task_id": task.get("task_id"), "scores": []}

    def _calculate_capability_score(
        self, requirements: List[str], capabilities: List[str]
    ) -> float:
        """Calculate how well logic source capabilities match task requirements"""
        if not requirements:
            return 0.5  # Neutral score if no specific requirements

        # Normalize to lowercase for comparison
        req_lower = [req.lower() for req in requirements]
        cap_lower = [cap.lower() for cap in capabilities]

        # Count matches
        matches = sum(1 for req in req_lower if any(req in cap for cap in cap_lower))

        # Calculate score based on match ratio
        match_ratio = matches / len(requirements)

        # Boost score for exact matches
        exact_matches = sum(1 for req in req_lower if req in cap_lower)
        exact_boost = exact_matches / len(requirements) * 0.2

        return min(match_ratio + exact_boost, 1.0)

    def _calculate_type_score(self, task_type: str, logic_source: str) -> float:
        """Calculate score based on task type and logic source specialization"""
        type_mappings = {
            "infrastructure": ["igris_logic"],
            "kubernetes": ["katie_logic"],
            "assistant": ["james_logic"],
            "ml_training": ["whis_logic"],
            "security": ["igris_logic"],
            "platform": ["igris_logic"],
            "voice": ["james_logic"],
            "image": ["james_logic"],
            "enhancement": ["whis_logic"],
            "deployment": ["katie_logic"],
            "scaling": ["katie_logic"],
            "analysis": ["igris_logic", "katie_logic"],
        }

        task_type_lower = task_type.lower()

        # Check for exact type match
        if task_type_lower in type_mappings:
            if logic_source in type_mappings[task_type_lower]:
                return 1.0
            else:
                return 0.3  # Low score for non-matching types

        # Check for partial matches
        for type_key, sources in type_mappings.items():
            if type_key in task_type_lower and logic_source in sources:
                return 0.8

        return 0.5  # Neutral score for unknown types

    def _calculate_priority_score(self, task_priority: str, logic_source: str) -> float:
        """Calculate score based on task priority and logic source priority handling"""
        priority_mappings = {
            "critical": {
                "whis_logic": 1.0,  # Whis handles critical ML tasks
                "katie_logic": 0.9,  # Katie handles critical K8s issues
                "igris_logic": 0.8,  # Igris handles critical infrastructure
                "james_logic": 0.7,  # James handles critical assistance
            },
            "high": {
                "katie_logic": 1.0,  # Katie excels at high-priority K8s ops
                "igris_logic": 0.9,  # Igris handles high-priority infrastructure
                "whis_logic": 0.8,  # Whis handles high-priority training
                "james_logic": 0.7,  # James handles high-priority assistance
            },
            "medium": {
                "james_logic": 1.0,  # James handles medium-priority tasks well
                "igris_logic": 0.9,  # Igris handles medium infrastructure
                "katie_logic": 0.8,  # Katie handles medium K8s tasks
                "whis_logic": 0.7,  # Whis handles medium training
            },
            "low": {
                "james_logic": 1.0,  # James handles low-priority tasks
                "whis_logic": 0.9,  # Whis can handle low-priority training
                "igris_logic": 0.8,  # Igris handles low infrastructure
                "katie_logic": 0.7,  # Katie handles low K8s tasks
            },
        }

        return priority_mappings.get(task_priority, {}).get(logic_source, 0.5)

    def _check_logic_source_availability(self, config: Dict[str, Any]) -> float:
        """Check if logic source is available and healthy"""
        try:
            health_url = f"{config['endpoint']}{config['health_endpoint']}"
            response = requests.get(health_url, timeout=5)

            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy":
                    return 1.0
                else:
                    return 0.5
            else:
                return 0.3

        except requests.exceptions.RequestException:
            return 0.0  # Unavailable
        except Exception:
            return 0.5  # Unknown status

    def _generate_recommendation(
        self, scores: List[Dict[str, Any]], task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate recommendation based on scoring results"""
        if not scores:
            return {
                "action": "reject",
                "reason": "No suitable logic sources available",
                "suggestion": "Review task requirements or check logic source availability",
            }

        best_score = scores[0]["total_score"]

        if best_score >= 0.8:
            return {
                "action": "approve",
                "logic_source": scores[0]["logic_source"],
                "confidence": "high",
                "reason": (
                    f"Excellent match with {scores[0]['name']} "
                    f"(score: {best_score:.2f})"
                ),
            }
        elif best_score >= 0.6:
            return {
                "action": "approve",
                "logic_source": scores[0]["logic_source"],
                "confidence": "medium",
                "reason": (
                    f"Good match with {scores[0]['name']} " f"(score: {best_score:.2f})"
                ),
            }
        elif best_score >= 0.4:
            return {
                "action": "approve_with_fallback",
                "logic_source": scores[0]["logic_source"],
                "confidence": "low",
                "reason": (
                    f"Moderate match with {scores[0]['name']} "
                    f"(score: {best_score:.2f}), will use fallback"
                ),
            }
        else:
            return {
                "action": "reject",
                "reason": (
                    f"Poor match with best logic source " f"(score: {best_score:.2f})"
                ),
                "suggestion": "Consider revising task requirements or adding new logic source",
            }

    def get_logic_source_capabilities(
        self, logic_source: str
    ) -> Optional[Dict[str, Any]]:
        """Get capabilities of a specific logic source"""
        return self.logic_sources.get(logic_source)

    def list_logic_sources(self) -> List[Dict[str, Any]]:
        """List all available logic sources"""
        return [
            {
                "logic_source": source,
                "name": config["name"],
                "description": config["description"],
                "capabilities": config["capabilities"],
                "endpoint": config["endpoint"],
            }
            for source, config in self.logic_sources.items()
        ]

    def validate_task_requirements(self, requirements: List[str]) -> Dict[str, Any]:
        """Validate task requirements against available capabilities"""
        all_capabilities = []
        for config in self.logic_sources.values():
            all_capabilities.extend(config["capabilities"])

        all_capabilities = list(set(all_capabilities))  # Remove duplicates

        # Check which requirements are covered
        covered_requirements = []
        uncovered_requirements = []

        for req in requirements:
            req_lower = req.lower()
            if any(req_lower in cap.lower() for cap in all_capabilities):
                covered_requirements.append(req)
            else:
                uncovered_requirements.append(req)

        coverage_ratio = (
            len(covered_requirements) / len(requirements) if requirements else 0
        )

        return {
            "total_requirements": len(requirements),
            "covered_requirements": covered_requirements,
            "uncovered_requirements": uncovered_requirements,
            "coverage_ratio": coverage_ratio,
            "available_capabilities": all_capabilities,
        }
