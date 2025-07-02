from typing import Dict, List, Any


class AuditScorer:
    def __init__(self):
        # Rule weights for different audit categories
        self.weights = {
            "gitops_readiness": 0.25,
            "security_signals": 0.30,
            "architecture_health": 0.20,
            "ci_cd_maturity": 0.15,
            "rbac_compliance": 0.10,
        }

        # Scoring thresholds
        self.thresholds = {"low_risk": 0.7, "medium_risk": 0.4, "high_risk": 0.0}

    def score_repository(self, repo_scan) -> Dict[str, Any]:
        """Score a repository based on audit criteria"""

        # Calculate individual category scores
        gitops_score = self._score_gitops_readiness(repo_scan)
        security_score = self._score_security_signals(repo_scan)
        architecture_score = self._score_architecture_health(repo_scan)
        ci_cd_score = self._score_ci_cd_maturity(repo_scan)
        rbac_score = self._score_rbac_compliance(repo_scan)

        # Calculate weighted overall score
        overall_score = (
            gitops_score * self.weights["gitops_readiness"]
            + security_score * self.weights["security_signals"]
            + architecture_score * self.weights["architecture_health"]
            + ci_cd_score * self.weights["ci_cd_maturity"]
            + rbac_score * self.weights["rbac_compliance"]
        )

        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)

        # Generate explanation and recommendations
        explanation = self._generate_explanation(
            gitops_score,
            security_score,
            architecture_score,
            ci_cd_score,
            rbac_score,
            overall_score,
        )

        recommendations = self._generate_recommendations(
            gitops_score, security_score, architecture_score, ci_cd_score, rbac_score
        )

        return {
            "overall_score": round(overall_score, 2),
            "risk_level": risk_level,
            "explanation": explanation,
            "breakdown": {
                "gitops_readiness": round(gitops_score, 2),
                "security_signals": round(security_score, 2),
                "architecture_health": round(architecture_score, 2),
                "ci_cd_maturity": round(ci_cd_score, 2),
                "rbac_compliance": round(rbac_score, 2),
            },
            "recommendations": recommendations,
        }

    def _score_gitops_readiness(self, repo_scan) -> float:
        """Score GitOps readiness based on tools and practices"""
        score = 0.0
        max_score = 100.0

        # Check for GitOps tools
        gitops_tools = repo_scan.gitops_tools
        if any(
            tool.get("name") in ["argocd", "flux", "tekton"] for tool in gitops_tools
        ):
            score += 30.0

        # Check for declarative configurations
        helm_charts = repo_scan.helm_charts
        if helm_charts:
            score += 25.0

        # Check for automated deployment configs
        ci_cd_files = repo_scan.ci_cd_files
        if any("deploy" in file.get("name", "").lower() for file in ci_cd_files):
            score += 25.0

        # Check for drift detection
        if any("monitor" in tool.get("name", "").lower() for tool in gitops_tools):
            score += 20.0

        return min(score, max_score) / max_score

    def _score_security_signals(self, repo_scan) -> float:
        """Score security based on issues and practices"""
        score = 100.0  # Start with perfect score, deduct for issues

        # Deduct for security issues
        security_issues = repo_scan.security_issues
        for issue in security_issues:
            severity = issue.get("severity", "medium")
            if severity == "high":
                score -= 25.0
            elif severity == "medium":
                score -= 15.0
            elif severity == "low":
                score -= 5.0

        # Check secrets management
        secrets_mgmt = repo_scan.secrets_management
        if not secrets_mgmt:
            score -= 20.0
        elif any(
            "plaintext" in secret.get("type", "").lower() for secret in secrets_mgmt
        ):
            score -= 15.0

        return max(score, 0.0) / 100.0

    def _score_architecture_health(self, repo_scan) -> float:
        """Score architecture based on patterns and modularity"""
        score = 0.0
        max_score = 100.0

        # Check for microservices patterns
        arch_patterns = repo_scan.architecture_patterns
        if any(
            "microservice" in pattern.get("type", "").lower()
            for pattern in arch_patterns
        ):
            score += 40.0
        elif any(
            "monolith" in pattern.get("type", "").lower() for pattern in arch_patterns
        ):
            score += 20.0

        # Check for service discovery
        if any(
            "service-mesh" in pattern.get("type", "").lower()
            for pattern in arch_patterns
        ):
            score += 20.0

        # Check for API gateway
        if any(
            "api-gateway" in pattern.get("type", "").lower()
            for pattern in arch_patterns
        ):
            score += 20.0

        # Check for health checks
        if any(
            "health-check" in pattern.get("type", "").lower()
            for pattern in arch_patterns
        ):
            score += 20.0

        return min(score, max_score) / max_score

    def _score_ci_cd_maturity(self, repo_scan) -> float:
        """Score CI/CD maturity"""
        score = 0.0
        max_score = 100.0

        ci_cd_files = repo_scan.ci_cd_files

        # Check for different CI/CD tools
        tools_found = set()
        for file in ci_cd_files:
            name = file.get("name", "").lower()
            if "github" in name or "actions" in name:
                tools_found.add("github")
            elif "jenkins" in name:
                tools_found.add("jenkins")
            elif "gitlab" in name:
                tools_found.add("gitlab")
            elif "tekton" in name:
                tools_found.add("tekton")

        score += len(tools_found) * 20.0

        # Check for pipeline stages
        stages_found = 0
        for file in ci_cd_files:
            content = file.get("content", "").lower()
            if any(stage in content for stage in ["lint", "test", "build", "deploy"]):
                stages_found += 1

        score += min(stages_found * 15.0, 60.0)

        return min(score, max_score) / max_score

    def _score_rbac_compliance(self, repo_scan) -> float:
        """Score RBAC compliance"""
        score = 0.0
        max_score = 100.0

        rbac_configs = repo_scan.rbac_configs

        if rbac_configs:
            score += 40.0

            # Check for role separation
            roles_found = set()
            for config in rbac_configs:
                content = config.get("content", "").lower()
                if "admin" in content:
                    roles_found.add("admin")
                if "developer" in content:
                    roles_found.add("developer")
                if "read" in content:
                    roles_found.add("readonly")

            score += len(roles_found) * 20.0

            # Check for service accounts
            if any(
                "serviceaccount" in config.get("content", "").lower()
                for config in rbac_configs
            ):
                score += 20.0

        return min(score, max_score) / max_score

    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= self.thresholds["low_risk"]:
            return "LOW"
        elif score >= self.thresholds["medium_risk"]:
            return "MEDIUM"
        else:
            return "HIGH"

    def _generate_explanation(
        self,
        gitops_score: float,
        security_score: float,
        architecture_score: float,
        ci_cd_score: float,
        rbac_score: float,
        overall_score: float,
    ) -> str:
        """Generate explanation for the audit score"""
        explanations = []

        if overall_score >= 0.8:
            explanations.append(
                "Excellent repository health with strong adherence to best practices."
            )
        elif overall_score >= 0.6:
            explanations.append(
                "Good repository health with room for improvement in specific areas."
            )
        elif overall_score >= 0.4:
            explanations.append(
                "Moderate repository health with several areas needing attention."
            )
        else:
            explanations.append(
                "Poor repository health requiring immediate attention and remediation."
            )

        # Add specific area explanations
        if gitops_score < 0.5:
            explanations.append(
                "GitOps practices need improvement - "
                "consider implementing ArgoCD or Flux."
            )
        if security_score < 0.6:
            explanations.append(
                "Security posture requires enhancement - review secrets "
                "management and access controls."
            )
        if architecture_score < 0.5:
            explanations.append(
                "Architecture could benefit from more modular design patterns."
            )

        return " ".join(explanations)

    def _generate_recommendations(
        self,
        gitops_score: float,
        security_score: float,
        architecture_score: float,
        ci_cd_score: float,
        rbac_score: float,
    ) -> List[str]:
        """Generate specific recommendations based on scores"""
        recommendations = []

        if gitops_score < 0.7:
            recommendations.extend(
                [
                    "Implement ArgoCD or Flux for GitOps deployments",
                    "Store all configurations declaratively in Git",
                    "Set up automated drift detection and remediation",
                ]
            )

        if security_score < 0.7:
            recommendations.extend(
                [
                    "Implement proper secrets management "
                    "(HashiCorp Vault, AWS Secrets Manager)",
                    "Review and fix security vulnerabilities",
                    "Enable RBAC and implement least privilege access",
                ]
            )

        if architecture_score < 0.6:
            recommendations.extend(
                [
                    "Consider breaking down monolith into microservices",
                    "Implement service mesh for service-to-service communication",
                    "Add health checks and circuit breakers for resilience",
                ]
            )

        if ci_cd_score < 0.6:
            recommendations.extend(
                [
                    "Implement comprehensive CI/CD pipeline with all stages",
                    "Add automated testing and security scanning",
                    "Set up environment-specific deployment strategies",
                ]
            )

        if rbac_score < 0.5:
            recommendations.extend(
                [
                    "Implement proper RBAC with role separation",
                    "Use dedicated service accounts for applications",
                    "Set up regular permission reviews and audits",
                ]
            )

        return list(set(recommendations))  # Remove duplicates

    def _score_confidence(self, factors: List[float]) -> Dict[str, Any]:
        """Calculate confidence based on a list of factors"""
        score = sum(factors) / len(factors)
        confidence = score
        return {
            "score": score,
            "confidence": confidence,
            "reasoning": (
                f"Based on {len(factors)} factors with " f"{confidence:.2f} confidence"
            ),
        }
