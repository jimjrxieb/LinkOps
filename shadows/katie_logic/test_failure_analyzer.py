"""
Test Failure Analyzer for Katie Logic
Uses response schema contracts to validate and fix test failures
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TestFailureAnalyzer:
    """
    Analyzes test failures and suggests fixes based on response schema contracts
    """

    def __init__(self):
        self.schemas = self._load_response_schemas()
        self.failure_patterns = self._load_failure_patterns()

    def _load_response_schemas(self) -> Dict[str, Any]:
        """Load response schema contracts"""
        schema_path = Path(__file__).parent / "response_schema_contracts.json"
        try:
            with open(schema_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Response schema contracts not found, using defaults")
            return {}

    def _load_failure_patterns(self) -> Dict[str, Any]:
        """Load failure detection patterns"""
        return {
            "assertion_failures": {
                "certification_check": {
                    "pattern": r'assert\s+"CKA"\s+in\s+data\["certifications"\]',
                    "fix": 'assert any("CKA" in cert for cert in data["certifications"])',
                    "description": "String subset matching in certifications",
                },
                "status_check": {
                    "pattern": r'assert\s+data\["status"\]\s*==\s*"dry_run"',
                    "fix": 'assert data["status"] == "dry_run"',
                    "description": "Status assertion for dry_run",
                },
            },
            "keyerror_failures": {
                "missing_pod_name": {
                    "pattern": r"KeyError:\s*'pod_name'",
                    "fix": 'Add "pod_name" field to response',
                    "description": "Missing pod_name in describe_pod response",
                },
                "missing_deployment_name": {
                    "pattern": r"KeyError:\s*'deployment_name'",
                    "fix": 'Add "deployment_name" field to response',
                    "description": "Missing deployment_name in describe_deployment response",
                },
                "missing_new_replicas": {
                    "pattern": r"KeyError:\s*'new_replicas'",
                    "fix": 'Add "new_replicas" field to response',
                    "description": "Missing new_replicas in scale_deployment response",
                },
                "missing_log_count": {
                    "pattern": r"KeyError:\s*'log_count'",
                    "fix": 'Add "log_count" field to response',
                    "description": "Missing log_count in get_pod_logs response",
                },
                "missing_patch_applied": {
                    "pattern": r"KeyError:\s*'patch_applied'",
                    "fix": 'Add "patch_applied" field to response',
                    "description": "Missing patch_applied in patch_deployment response",
                },
            },
        }

    def analyze_test_failure(
        self, test_name: str, error_message: str, traceback: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze a test failure and suggest fixes
        """
        logger.info(f"Analyzing test failure: {test_name}")

        analysis = {
            "test_name": test_name,
            "failure_type": self._detect_failure_type(error_message),
            "suggested_fixes": [],
            "schema_violations": [],
            "priority": "medium",
        }

        # Detect specific failure patterns
        pattern_matches = self._match_failure_patterns(error_message)
        for pattern_type, matches in pattern_matches.items():
            for match in matches:
                analysis["suggested_fixes"].append(
                    {
                        "type": pattern_type,
                        "description": match["description"],
                        "fix": match["fix"],
                        "file": self._identify_target_file(test_name),
                        "line_hint": self._extract_line_hint(traceback),
                    }
                )

        # Check schema violations
        schema_violations = self._check_schema_violations(test_name, error_message)
        analysis["schema_violations"] = schema_violations

        # Set priority based on failure type
        if "KeyError" in error_message:
            analysis["priority"] = "high"
        elif "assertion" in error_message.lower():
            analysis["priority"] = "medium"
        else:
            analysis["priority"] = "low"

        return analysis

    def _detect_failure_type(self, error_message: str) -> str:
        """Detect the type of test failure"""
        if "KeyError" in error_message:
            return "keyerror"
        elif "AssertionError" in error_message:
            return "assertion"
        elif "ImportError" in error_message:
            return "import"
        elif "ModuleNotFoundError" in error_message:
            return "import"
        else:
            return "unknown"

    def _match_failure_patterns(
        self, error_message: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Match error message against known failure patterns"""
        matches = {"assertion_failures": [], "keyerror_failures": []}

        for pattern_type, patterns in self.failure_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                if re.search(pattern_data["pattern"], error_message):
                    matches[pattern_type].append(
                        {
                            "name": pattern_name,
                            "description": pattern_data["description"],
                            "fix": pattern_data["fix"],
                        }
                    )

        return matches

    def _check_schema_violations(
        self, test_name: str, error_message: str
    ) -> List[Dict[str, Any]]:
        """Check for schema violations based on test name"""
        violations = []

        # Map test names to schema endpoints
        test_to_schema = {
            "test_health_check": "health_endpoint",
            "test_get_capabilities": "capabilities_endpoint",
            "test_describe_pod_analysis": "describe_pod",
            "test_describe_deployment_analysis": "describe_deployment",
            "test_scale_deployment_analysis": "scale_deployment",
            "test_scale_deployment_dry_run": "scale_deployment",
            "test_log_analysis": "get_pod_logs",
            "test_patch_validation": "patch_deployment",
        }

        schema_key = test_to_schema.get(test_name)
        if schema_key and schema_key in self.schemas:
            schema = self.schemas[schema_key]
            required_fields = schema.get("required_fields", [])

            # Check for missing required fields
            for field in required_fields:
                if f"KeyError: '{field}'" in error_message:
                    violations.append(
                        {
                            "field": field,
                            "type": "missing_required_field",
                            "schema": schema_key,
                            "fix": f"Add '{field}' field to response",
                        }
                    )

        return violations

    def _identify_target_file(self, test_name: str) -> str:
        """Identify the target file that needs to be fixed"""
        test_to_file = {
            "test_health_check": "main.py",
            "test_get_capabilities": "main.py",
            "test_describe_pod_analysis": "kubeops/describe.py",
            "test_describe_deployment_analysis": "kubeops/describe.py",
            "test_scale_deployment_analysis": "kubeops/scale.py",
            "test_scale_deployment_dry_run": "kubeops/scale.py",
            "test_log_analysis": "kubeops/logs.py",
            "test_patch_validation": "kubeops/patch.py",
        }
        return test_to_file.get(test_name, "unknown")

    def _extract_line_hint(self, traceback: str) -> Optional[int]:
        """Extract line number hint from traceback"""
        if not traceback:
            return None

        # Look for line number in traceback
        line_match = re.search(r"line (\d+)", traceback)
        if line_match:
            return int(line_match.group(1))
        return None

    def generate_fix_suggestion(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive fix suggestion"""
        if not analysis["suggested_fixes"]:
            return "# No specific fix pattern detected. Review test and implementation manually."

        fix_suggestion = f"""
# Fix for {analysis['test_name']}
# Priority: {analysis['priority']}
# Failure Type: {analysis['failure_type']}

"""

        for fix in analysis["suggested_fixes"]:
            fix_suggestion += f"""
## {fix['description']}
# File: {fix['file']}
{fix['fix']}

"""

        if analysis["schema_violations"]:
            fix_suggestion += "\n## Schema Violations:\n"
            for violation in analysis["schema_violations"]:
                fix_suggestion += f"# - {violation['fix']}\n"

        return fix_suggestion

    def validate_response_against_schema(
        self, endpoint: str, response: Dict[str, Any]
    ) -> List[str]:
        """Validate a response against its schema"""
        violations = []

        if endpoint not in self.schemas:
            return [f"Unknown endpoint: {endpoint}"]

        schema = self.schemas[endpoint]
        required_fields = schema.get("required_fields", [])

        for field in required_fields:
            if field not in response:
                violations.append(f"Missing required field: {field}")

        return violations

    def get_schema_for_endpoint(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Get schema for a specific endpoint"""
        return self.schemas.get(endpoint)


# Global instance
test_failure_analyzer = TestFailureAnalyzer()
