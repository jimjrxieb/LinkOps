"""
Orbs and Runes System - ML Knowledge Representation
Handles ML knowledge as Orbs (concepts) and Runes (executable patterns)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np


class Orb:
    """Orb represents a high-level ML concept or knowledge domain"""

    def __init__(
        self, name: str, description: str, domain: str, confidence: float = 0.0
    ):
        self.name = name
        self.description = description
        self.domain = domain
        self.confidence = confidence
        self.runes = []
        self.metadata = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_rune(self, rune: "Rune"):
        """Add a Rune to this Orb"""
        self.runes.append(rune)
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert Orb to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "confidence": self.confidence,
            "runes": [rune.to_dict() for rune in self.runes],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Rune:
    """Rune represents an executable ML pattern or solution"""

    def __init__(self, name: str, pattern: str, code: str, metadata: Dict[str, Any]):
        self.name = name
        self.pattern = pattern
        self.code = code
        self.metadata = metadata
        self.success_rate = 0.0
        self.usage_count = 0
        self.feedback_score = 0.0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Rune with given context"""
        self.usage_count += 1
        self.updated_at = datetime.now()

        # This would execute the actual code pattern
        # For now, return a simulated result
        return {
            "rune_name": self.name,
            "execution_status": "success",
            "result": f"Executed {self.pattern} with context: {context}",
            "metadata": self.metadata,
        }

    def update_feedback(self, score: float):
        """Update Rune with feedback score"""
        self.feedback_score = (self.feedback_score + score) / 2
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert Rune to dictionary"""
        return {
            "name": self.name,
            "pattern": self.pattern,
            "code": self.code,
            "metadata": self.metadata,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count,
            "feedback_score": self.feedback_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class OrbsRunesSystem:
    """Central system for managing Orbs and Runes"""

    def __init__(self):
        self.orbs = {}
        self.runes = {}
        self.learning_history = []
        self.feedback_system = {}
        self.openai_fallback = True

        # Initialize with common ML Orbs
        self._initialize_ml_orbs()

    def create_orb(self, name: str, description: str, domain: str) -> Orb:
        """Create a new Orb"""
        orb = Orb(name, description, domain)
        self.orbs[name] = orb
        return orb

    def create_rune(
        self, name: str, pattern: str, code: str, metadata: Dict[str, Any]
    ) -> Rune:
        """Create a new Rune"""
        rune = Rune(name, pattern, code, metadata)
        self.runes[name] = rune
        return rune

    def add_rune_to_orb(self, orb_name: str, rune_name: str):
        """Add a Rune to an Orb"""
        if orb_name in self.orbs and rune_name in self.runes:
            self.orbs[orb_name].add_rune(self.runes[rune_name])

    def find_matching_rune(
        self, task_description: str, context: Dict[str, Any]
    ) -> Optional[Rune]:
        """Find the best matching Rune for a task"""
        best_rune = None
        best_score = 0.0

        for rune in self.runes.values():
            score = self._calculate_rune_match_score(rune, task_description, context)
            if score > best_score:
                best_score = score
                best_rune = rune

        # If no good match found and OpenAI fallback is enabled
        if best_score < 0.7 and self.openai_fallback:
            return self._create_openai_fallback_rune(task_description, context)

        return best_rune

    def learn_from_task(
        self,
        task_description: str,
        solution_path: List[Dict[str, Any]],
        success: bool,
        feedback: Dict[str, Any],
    ):
        """Learn from a completed task and update Orbs/Runes"""
        learning_record = {
            "task_description": task_description,
            "solution_path": solution_path,
            "success": success,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
        }

        self.learning_history.append(learning_record)

        # Extract patterns from solution path
        patterns = self._extract_patterns_from_solution(solution_path)

        # Update existing Runes or create new ones
        for pattern in patterns:
            self._update_or_create_rune(pattern, success, feedback)

        # Update Orb confidence based on learning
        self._update_orb_confidence(task_description, success)

    def learn_from_feedback(
        self, rune_name: str, feedback_score: float, feedback_details: Dict[str, Any]
    ):
        """Learn from user feedback on a Rune"""
        if rune_name in self.runes:
            self.runes[rune_name].update_feedback(feedback_score)

            # Store detailed feedback
            self.feedback_system[rune_name] = {
                "score": feedback_score,
                "details": feedback_details,
                "timestamp": datetime.now().isoformat(),
            }

    def learn_from_test_failures(self, test_results: List[Dict[str, Any]]):
        """Learn from test failures to improve Runes"""
        for test_result in test_results:
            if not test_result.get("passed", True):
                failure_pattern = self._extract_failure_pattern(test_result)
                self._create_failure_recovery_rune(failure_pattern, test_result)

    def convert_solution_to_rune(
        self, solution_path: List[Dict[str, Any]], task_type: str
    ) -> Rune:
        """Convert a sample solution path into an executable Rune"""
        # Extract the pattern from solution path
        pattern = self._extract_pattern_from_solution(solution_path)

        # Generate executable code
        code = self._generate_executable_code(solution_path, task_type)

        # Create metadata
        metadata = {
            "task_type": task_type,
            "solution_steps": len(solution_path),
            "complexity": self._calculate_solution_complexity(solution_path),
            "estimated_execution_time": self._estimate_execution_time(solution_path),
        }

        # Create Rune
        rune_name = f"{task_type}_solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        rune = self.create_rune(rune_name, pattern, code, metadata)

        return rune

    def get_orb_knowledge(self, orb_name: str) -> Dict[str, Any]:
        """Get comprehensive knowledge from an Orb"""
        if orb_name not in self.orbs:
            return {"error": "Orb not found"}

        orb = self.orbs[orb_name]
        return {
            "orb": orb.to_dict(),
            "total_runes": len(orb.runes),
            "average_confidence": (
                np.mean([rune.feedback_score for rune in orb.runes])
                if orb.runes
                else 0.0
            ),
            "most_used_rune": (
                max(orb.runes, key=lambda r: r.usage_count).name if orb.runes else None
            ),
            "recent_learning": self._get_recent_learning_for_orb(orb_name),
        }

    def search_orbs(self, query: str) -> List[Dict[str, Any]]:
        """Search Orbs by query"""
        results = []
        query_lower = query.lower()

        for orb_name, orb in self.orbs.items():
            if (
                query_lower in orb.name.lower()
                or query_lower in orb.description.lower()
                or query_lower in orb.domain.lower()
            ):
                results.append(
                    {
                        "orb_name": orb_name,
                        "orb": orb.to_dict(),
                        "relevance_score": self._calculate_search_relevance(orb, query),
                    }
                )

        return sorted(results, key=lambda x: x["relevance_score"], reverse=True)

    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning history"""
        if not self.learning_history:
            return {"message": "No learning history available"}

        insights = {
            "total_tasks": len(self.learning_history),
            "success_rate": sum(
                1 for record in self.learning_history if record["success"]
            )
            / len(self.learning_history),
            "most_common_patterns": self._find_most_common_patterns(),
            "learning_trends": self._analyze_learning_trends(),
            "improvement_areas": self._identify_improvement_areas(),
        }

        return insights

    def _initialize_ml_orbs(self):
        """Initialize common ML Orbs"""
        ml_orbs = [
            {
                "name": "data_preprocessing",
                "description": "Data cleaning, transformation, and feature engineering",
                "domain": "data_engineering",
            },
            {
                "name": "model_training",
                "description": "Supervised and unsupervised model training",
                "domain": "machine_learning",
            },
            {
                "name": "model_evaluation",
                "description": "Model performance evaluation and bias detection",
                "domain": "mlops",
            },
            {
                "name": "model_deployment",
                "description": "Model serving and deployment strategies",
                "domain": "mlops",
            },
            {
                "name": "experiment_tracking",
                "description": "ML experiment tracking and versioning",
                "domain": "mlops",
            },
            {
                "name": "feature_engineering",
                "description": "Feature extraction and selection techniques",
                "domain": "machine_learning",
            },
        ]

        for orb_config in ml_orbs:
            self.create_orb(
                orb_config["name"], orb_config["description"], orb_config["domain"]
            )

    def _calculate_rune_match_score(
        self, rune: Rune, task_description: str, context: Dict[str, Any]
    ) -> float:
        """Calculate how well a Rune matches a task"""
        score = 0.0

        # Pattern matching
        if rune.pattern.lower() in task_description.lower():
            score += 0.4

        # Metadata matching
        for key, value in context.items():
            if key in rune.metadata and rune.metadata[key] == value:
                score += 0.2

        # Feedback score influence
        score += rune.feedback_score * 0.3

        # Usage count influence (more usage = more reliable)
        score += min(rune.usage_count / 100, 0.1)

        return min(score, 1.0)

    def _create_openai_fallback_rune(
        self, task_description: str, context: Dict[str, Any]
    ) -> Rune:
        """Create a fallback Rune using OpenAI"""
        # This would integrate with OpenAI API
        # For now, create a generic fallback Rune
        fallback_rune = Rune(
            name=f"openai_fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            pattern="openai_generated_solution",
            code="openai.generate_solution(task_description, context)",
            metadata={
                "source": "openai",
                "task_description": task_description,
                "context": context,
            },
        )

        return fallback_rune

    def _extract_patterns_from_solution(
        self, solution_path: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract patterns from a solution path"""
        patterns = []

        for step in solution_path:
            if "operation" in step:
                patterns.append(step["operation"])
            if "method" in step:
                patterns.append(step["method"])

        return list(set(patterns))  # Remove duplicates

    def _update_or_create_rune(
        self, pattern: str, success: bool, feedback: Dict[str, Any]
    ):
        """Update existing Rune or create new one based on pattern"""
        # Find existing Rune with similar pattern
        existing_rune = None
        for rune in self.runes.values():
            if pattern.lower() in rune.pattern.lower():
                existing_rune = rune
                break

        if existing_rune:
            # Update existing Rune
            feedback_score = 1.0 if success else 0.0
            existing_rune.update_feedback(feedback_score)
        else:
            # Create new Rune
            new_rune = Rune(
                name=f"learned_{pattern}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                pattern=pattern,
                code=f"# Generated code for {pattern}",
                metadata={"source": "learned", "success": success},
            )
            self.runes[new_rune.name] = new_rune

    def _update_orb_confidence(self, task_description: str, success: bool):
        """Update Orb confidence based on task success"""
        # Find relevant Orbs and update their confidence
        for orb_name, orb in self.orbs.items():
            if orb_name.lower() in task_description.lower():
                if success:
                    orb.confidence = min(orb.confidence + 0.1, 1.0)
                else:
                    orb.confidence = max(orb.confidence - 0.05, 0.0)

    def _extract_failure_pattern(self, test_result: Dict[str, Any]) -> str:
        """Extract failure pattern from test result"""
        error_message = test_result.get("error", "")
        test_name = test_result.get("test_name", "")

        # Extract key failure indicators
        failure_indicators = []
        if "assertion" in error_message.lower():
            failure_indicators.append("assertion_failure")
        if "timeout" in error_message.lower():
            failure_indicators.append("timeout")
        if "memory" in error_message.lower():
            failure_indicators.append("memory_error")

        return f"{test_name}_{'_'.join(failure_indicators)}"

    def _create_failure_recovery_rune(
        self, failure_pattern: str, test_result: Dict[str, Any]
    ):
        """Create a Rune for handling test failures"""
        recovery_rune = Rune(
            name=f"recovery_{failure_pattern}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            pattern=failure_pattern,
            code=f"# Recovery code for {failure_pattern}",
            metadata={
                "type": "failure_recovery",
                "test_result": test_result,
                "created_from_failure": True,
            },
        )

        self.runes[recovery_rune.name] = recovery_rune

    def _extract_pattern_from_solution(
        self, solution_path: List[Dict[str, Any]]
    ) -> str:
        """Extract a pattern from solution path"""
        operations = []
        for step in solution_path:
            if "operation" in step:
                operations.append(step["operation"])

        return " -> ".join(operations)

    def _generate_executable_code(
        self, solution_path: List[Dict[str, Any]], task_type: str
    ) -> str:
        """Generate executable code from solution path"""
        code_lines = [f"# Generated code for {task_type}"]
        code_lines.append("def execute_solution(context):")
        code_lines.append("    result = {}")

        for i, step in enumerate(solution_path):
            operation = step.get("operation", "unknown")
            code_lines.append(f"    # Step {i+1}: {operation}")
            code_lines.append(
                f"    result['step_{i+1}'] = execute_{operation}(context)"
            )

        code_lines.append("    return result")

        return "\n".join(code_lines)

    def _calculate_solution_complexity(
        self, solution_path: List[Dict[str, Any]]
    ) -> str:
        """Calculate solution complexity"""
        steps = len(solution_path)
        if steps <= 3:
            return "low"
        elif steps <= 7:
            return "medium"
        else:
            return "high"

    def _estimate_execution_time(self, solution_path: List[Dict[str, Any]]) -> int:
        """Estimate execution time in seconds"""
        base_time = len(solution_path) * 5  # 5 seconds per step
        return base_time

    def _get_recent_learning_for_orb(self, orb_name: str) -> List[Dict[str, Any]]:
        """Get recent learning records for an Orb"""
        recent_learning = []

        for record in self.learning_history[-10:]:  # Last 10 records
            if orb_name.lower() in record["task_description"].lower():
                recent_learning.append(record)

        return recent_learning

    def _calculate_search_relevance(self, orb: Orb, query: str) -> float:
        """Calculate search relevance score"""
        score = 0.0
        query_lower = query.lower()

        if query_lower in orb.name.lower():
            score += 0.5
        if query_lower in orb.description.lower():
            score += 0.3
        if query_lower in orb.domain.lower():
            score += 0.2

        return score

    def _find_most_common_patterns(self) -> List[Dict[str, Any]]:
        """Find most common patterns in learning history"""
        pattern_counts = {}

        for record in self.learning_history:
            patterns = self._extract_patterns_from_solution(record["solution_path"])
            for pattern in patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        # Return top 5 patterns
        sorted_patterns = sorted(
            pattern_counts.items(), key=lambda x: x[1], reverse=True
        )
        return [
            {"pattern": pattern, "count": count}
            for pattern, count in sorted_patterns[:5]
        ]

    def _analyze_learning_trends(self) -> Dict[str, Any]:
        """Analyze learning trends over time"""
        if len(self.learning_history) < 2:
            return {"message": "Insufficient data for trend analysis"}

        # Calculate success rate trend
        recent_success_rate = (
            sum(1 for record in self.learning_history[-10:] if record["success"]) / 10
        )
        overall_success_rate = sum(
            1 for record in self.learning_history if record["success"]
        ) / len(self.learning_history)

        trend = (
            "improving" if recent_success_rate > overall_success_rate else "declining"
        )

        return {
            "trend": trend,
            "recent_success_rate": recent_success_rate,
            "overall_success_rate": overall_success_rate,
        }

    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas for improvement"""
        improvement_areas = []

        # Analyze Rune feedback scores
        low_feedback_runes = [
            rune for rune in self.runes.values() if rune.feedback_score < 0.5
        ]
        if low_feedback_runes:
            improvement_areas.append(
                f"{len(low_feedback_runes)} Runes need improvement"
            )

        # Analyze Orb confidence
        low_confidence_orbs = [
            orb for orb in self.orbs.values() if orb.confidence < 0.5
        ]
        if low_confidence_orbs:
            improvement_areas.append(
                f"{len(low_confidence_orbs)} Orbs need more learning"
            )

        return improvement_areas


# Global instance
orbs_runes_system = OrbsRunesSystem()
