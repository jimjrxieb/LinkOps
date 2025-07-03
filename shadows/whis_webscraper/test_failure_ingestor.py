"""
Test Failure Ingestor for Whis WebScraper
Captures test failures and generates structured fixes as Runes
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class TestFailure:
    """Structured test failure data"""

    test_name: str
    service: str
    failure_type: str  # assertion, keyerror, import, etc.
    assertion_failed: str
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    traceback: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    status: str = "pending_approval"
    created_at: str = None
    approved_at: Optional[str] = None
    applied_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


class TestFailureIngestor:
    """
    Ingests test failures and generates structured fixes
    """

    def __init__(self):
        self.failures_db: List[TestFailure] = []
        self.fix_patterns = self._load_fix_patterns()

    def ingest_failure(self, failure_data: Dict[str, Any]) -> TestFailure:
        """
        Ingest a test failure and generate a suggested fix
        """
        logger.info(
            f"Ingesting test failure: {failure_data.get('test_name', 'unknown')}"
        )

        # Create structured failure object
        failure = TestFailure(
            test_name=failure_data.get("test_name", "unknown"),
            service=failure_data.get("service", "unknown"),
            failure_type=failure_data.get("failure_type", "unknown"),
            assertion_failed=failure_data.get("assertion_failed", ""),
            expected_value=failure_data.get("expected_value"),
            actual_value=failure_data.get("actual_value"),
            traceback=failure_data.get("traceback"),
            file_path=failure_data.get("file_path"),
            line_number=failure_data.get("line_number"),
        )

        # Generate suggested fix
        failure.suggested_fix = self._generate_fix_suggestion(failure)

        # Store failure
        self.failures_db.append(failure)

        logger.info(f"Generated fix suggestion for {failure.test_name}")
        return failure

    def _generate_fix_suggestion(self, failure: TestFailure) -> str:
        """
        Generate a suggested fix based on failure type and patterns
        """
        if failure.failure_type == "assertion":
            return self._generate_assertion_fix(failure)
        elif failure.failure_type == "keyerror":
            return self._generate_keyerror_fix(failure)
        elif failure.failure_type == "import":
            return self._generate_import_fix(failure)
        else:
            return self._generate_generic_fix(failure)

    def _generate_assertion_fix(self, failure: TestFailure) -> str:
        """
        Generate fix for assertion failures
        """
        assertion = failure.assertion_failed.lower()

        # Handle string subset assertions
        if "in" in assertion and "certifications" in assertion:
            return """
# Fix: Use any() for string subset matching
# Before: assert "CKA" in data["certifications"]
# After: assert any("CKA" in cert for cert in data["certifications"])

# Update test assertion:
assert any("CKA" in cert for cert in data["certifications"])
"""

        # Handle status assertions
        elif "status" in assertion and "dry_run" in assertion:
            return """
# Fix: Ensure dry_run returns correct status
# In scale.py, update dry_run logic:
if dry_run:
    return {
        "agent": "katie",
        "status": "dry_run",
        "new_replicas": replicas
    }
"""

        return f"# Generic assertion fix for: {failure.assertion_failed}"

    def _generate_keyerror_fix(self, failure: TestFailure) -> str:
        """
        Generate fix for KeyError failures
        """
        missing_key = (
            failure.assertion_failed.split("'")[1]
            if "'" in failure.assertion_failed
            else "unknown"
        )

        return f"""
# Fix: Add missing key '{missing_key}' to response
# Update service function to include required field:

return {{
    "agent": "katie",
    "{missing_key}": value,  # Add this field
    "status": "success",
    # ... other fields
}}
"""

    def _generate_import_fix(self, failure: TestFailure) -> str:
        """
        Generate fix for import failures
        """
        return """
# Fix: Add proper import path setup
# Add to test file:

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # noqa: E402
"""

    def _generate_generic_fix(self, failure: TestFailure) -> str:
        """
        Generate generic fix suggestion
        """
        return f"""
# Generic fix for {failure.failure_type} failure
# Test: {failure.test_name}
# Assertion: {failure.assertion_failed}
# Review the test and service implementation for compatibility
"""

    def get_pending_failures(self) -> List[TestFailure]:
        """Get all pending failures awaiting approval"""
        return [f for f in self.failures_db if f.status == "pending_approval"]

    def approve_failure(self, test_name: str) -> bool:
        """Approve a failure fix"""
        for failure in self.failures_db:
            if failure.test_name == test_name and failure.status == "pending_approval":
                failure.status = "approved"
                failure.approved_at = datetime.utcnow().isoformat()
                logger.info(f"Approved fix for {test_name}")
                return True
        return False

    def reject_failure(self, test_name: str, reason: str = "") -> bool:
        """Reject a failure fix"""
        for failure in self.failures_db:
            if failure.test_name == test_name and failure.status == "pending_approval":
                failure.status = "rejected"
                failure.suggested_fix = f"REJECTED: {reason}\n\n{failure.suggested_fix}"
                logger.info(f"Rejected fix for {test_name}: {reason}")
                return True
        return False

    def mark_applied(self, test_name: str) -> bool:
        """Mark a fix as applied"""
        for failure in self.failures_db:
            if failure.test_name == test_name and failure.status == "approved":
                failure.status = "applied"
                failure.applied_at = datetime.utcnow().isoformat()
                logger.info(f"Marked fix as applied for {test_name}")
                return True
        return False

    def _load_fix_patterns(self) -> Dict[str, Any]:
        """Load fix patterns from configuration"""
        return {
            "assertion_patterns": {
                "string_subset": {
                    "pattern": r'assert\s+"([^"]+)"\s+in\s+data\["([^"]+)"\]',
                    "fix_template": 'assert any("{key}" in item for item in data["{field}"])',
                },
                "status_check": {
                    "pattern": r'assert\s+data\["status"\]\s*==\s*"([^"]+)"',
                    "fix_template": 'if condition:\n    return {{"status": "{expected_status}"}}',
                },
            },
            "keyerror_patterns": {
                "missing_field": {
                    "pattern": r"KeyError:\s*'([^']+)'",
                    "fix_template": 'return {{"{field}": value, "status": "success"}}',
                }
            },
        }

    def export_failures(self) -> str:
        """Export failures as JSON for Katie Logic"""
        return json.dumps([asdict(f) for f in self.failures_db], indent=2)

    def import_failures(self, failures_json: str) -> None:
        """Import failures from JSON"""
        failures_data = json.loads(failures_json)
        for failure_data in failures_data:
            failure = TestFailure(**failure_data)
            self.failures_db.append(failure)


# Global instance
test_failure_ingestor = TestFailureIngestor()
