"""
CKS Security Module - Certified Kubernetes Security Specialist
Elite Kubernetes security capabilities including policies, compliance, and threat detection
"""

from typing import Dict, List, Any


class CKSSecurity:
    """Certified Kubernetes Security Specialist operations"""

    def __init__(self):
        self.security_domains = {
            "cluster_hardening": {
                "rbac": "Role-based access control implementation",
                "network_policies": "Network security policies",
                "pod_security": "Pod security policies and standards",
                "secrets_management": "Secret storage and encryption",
            },
            "threat_detection": {
                "audit_logging": "Audit log analysis and monitoring",
                "runtime_security": "Runtime threat detection",
                "vulnerability_scanning": "Container and image scanning",
                "compliance_monitoring": "Compliance and policy enforcement",
            },
            "secure_development": {
                "image_security": "Container image security",
                "supply_chain": "Software supply chain security",
                "code_analysis": "Static code analysis",
                "secure_deployment": "Secure deployment practices",
            },
        }

    def analyze_cluster_security(
        self, cluster_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze overall cluster security posture"""
        security_analysis = {
            "overall_score": 0,
            "security_status": "secure",
            "vulnerabilities": [],
            "compliance_gaps": [],
            "recommendations": [],
            "risk_level": "low",
        }

        # Check RBAC configuration
        rbac_analysis = self._analyze_rbac_security(cluster_config.get("rbac", {}))
        security_analysis["rbac"] = rbac_analysis

        # Check network policies
        network_analysis = self._analyze_network_security(
            cluster_config.get("network_policies", [])
        )
        security_analysis["network"] = network_analysis

        # Check pod security
        pod_security_analysis = self._analyze_pod_security(
            cluster_config.get("pods", [])
        )
        security_analysis["pod_security"] = pod_security_analysis

        # Check secrets management
        secrets_analysis = self._analyze_secrets_management(
            cluster_config.get("secrets", [])
        )
        security_analysis["secrets"] = secrets_analysis

        # Calculate overall score
        security_analysis["overall_score"] = self._calculate_security_score(
            security_analysis
        )
        security_analysis["security_status"] = self._determine_security_status(
            security_analysis["overall_score"]
        )
        security_analysis["risk_level"] = self._determine_risk_level(security_analysis)

        # Generate recommendations
        security_analysis["recommendations"] = self._generate_security_recommendations(
            security_analysis
        )

        return security_analysis

    def enforce_security_policies(
        self, namespace: str, policy_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enforce security policies in a namespace"""
        enforcement = {
            "policy_type": policy_type,
            "namespace": namespace,
            "applied_policies": [],
            "compliance_status": "compliant",
            "violations": [],
        }

        if policy_type == "network_policy":
            enforcement["applied_policies"] = self._create_network_policies(
                namespace, config
            )
        elif policy_type == "pod_security":
            enforcement["applied_policies"] = self._create_pod_security_policies(
                namespace, config
            )
        elif policy_type == "rbac":
            enforcement["applied_policies"] = self._create_rbac_policies(
                namespace, config
            )
        elif policy_type == "admission_controller":
            enforcement["applied_policies"] = (
                self._create_admission_controller_policies(namespace, config)
            )

        return enforcement

    def scan_for_vulnerabilities(
        self, resources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Scan Kubernetes resources for security vulnerabilities"""
        vulnerability_scan = {
            "total_resources": len(resources),
            "vulnerabilities_found": 0,
            "critical_vulnerabilities": [],
            "high_vulnerabilities": [],
            "medium_vulnerabilities": [],
            "low_vulnerabilities": [],
            "recommendations": [],
        }

        for resource in resources:
            resource_vulns = self._scan_resource_vulnerabilities(resource)

            vulnerability_scan["critical_vulnerabilities"].extend(
                resource_vulns["critical"]
            )
            vulnerability_scan["high_vulnerabilities"].extend(resource_vulns["high"])
            vulnerability_scan["medium_vulnerabilities"].extend(
                resource_vulns["medium"]
            )
            vulnerability_scan["low_vulnerabilities"].extend(resource_vulns["low"])

        vulnerability_scan["vulnerabilities_found"] = (
            len(vulnerability_scan["critical_vulnerabilities"])
            + len(vulnerability_scan["high_vulnerabilities"])
            + len(vulnerability_scan["medium_vulnerabilities"])
            + len(vulnerability_scan["low_vulnerabilities"])
        )

        vulnerability_scan["recommendations"] = (
            self._generate_vulnerability_recommendations(vulnerability_scan)
        )

        return vulnerability_scan

    def audit_compliance(
        self, cluster_config: Dict[str, Any], compliance_standard: str
    ) -> Dict[str, Any]:
        """Audit cluster compliance against security standards"""
        compliance_audit = {
            "standard": compliance_standard,
            "overall_compliance": "compliant",
            "compliance_score": 0,
            "passed_checks": [],
            "failed_checks": [],
            "warnings": [],
            "recommendations": [],
        }

        if compliance_standard == "cis":
            compliance_audit.update(self._audit_cis_compliance(cluster_config))
        elif compliance_standard == "nist":
            compliance_audit.update(self._audit_nist_compliance(cluster_config))
        elif compliance_standard == "sox":
            compliance_audit.update(self._audit_sox_compliance(cluster_config))

        return compliance_audit

    def detect_threats(
        self, cluster_events: List[Dict[str, Any]], logs: List[str]
    ) -> Dict[str, Any]:
        """Detect security threats in cluster events and logs"""
        threat_detection = {
            "threats_detected": 0,
            "critical_threats": [],
            "high_threats": [],
            "medium_threats": [],
            "low_threats": [],
            "anomalies": [],
            "recommendations": [],
        }

        # Analyze cluster events
        event_threats = self._analyze_event_threats(cluster_events)
        threat_detection["critical_threats"].extend(event_threats["critical"])
        threat_detection["high_threats"].extend(event_threats["high"])

        # Analyze logs
        log_threats = self._analyze_log_threats(logs)
        threat_detection["critical_threats"].extend(log_threats["critical"])
        threat_detection["high_threats"].extend(log_threats["high"])

        # Detect anomalies
        threat_detection["anomalies"] = self._detect_anomalies(cluster_events, logs)

        threat_detection["threats_detected"] = (
            len(threat_detection["critical_threats"])
            + len(threat_detection["high_threats"])
            + len(threat_detection["medium_threats"])
            + len(threat_detection["low_threats"])
        )

        threat_detection["recommendations"] = self._generate_threat_recommendations(
            threat_detection
        )

        return threat_detection

    def secure_container_runtime(
        self, container_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Secure container runtime configuration"""
        runtime_security = {
            "security_context": {},
            "capabilities": [],
            "seccomp_profile": "",
            "apparmor_profile": "",
            "read_only_root": False,
            "non_root_user": False,
            "recommendations": [],
        }

        # Generate secure security context
        runtime_security["security_context"] = {
            "runAsNonRoot": True,
            "runAsUser": 1000,
            "runAsGroup": 3000,
            "fsGroup": 2000,
            "allowPrivilegeEscalation": False,
            "readOnlyRootFilesystem": True,
            "capabilities": {"drop": ["ALL"]},
        }

        # Generate recommendations
        runtime_security["recommendations"] = [
            "Run containers as non-root user",
            "Use read-only root filesystem",
            "Drop unnecessary capabilities",
            "Implement seccomp profiles",
            "Use AppArmor profiles",
            "Limit resource usage",
        ]

        return runtime_security

    def implement_secrets_management(
        self, secrets_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implement secure secrets management"""
        secrets_management = {
            "encryption_at_rest": False,
            "encryption_in_transit": False,
            "external_secrets": False,
            "rotation_policy": "",
            "access_controls": [],
            "recommendations": [],
        }

        # Check encryption configuration
        if secrets_config.get("encryption_provider"):
            secrets_management["encryption_at_rest"] = True

        # Generate recommendations
        secrets_management["recommendations"] = [
            "Enable encryption at rest for etcd",
            "Use external secrets management (HashiCorp Vault, AWS Secrets Manager)",
            "Implement automatic secret rotation",
            "Use RBAC to control secret access",
            "Audit secret access regularly",
            "Use Kubernetes secrets only for non-sensitive data",
        ]

        return secrets_management

    def configure_network_security(
        self, network_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Configure network security policies"""
        network_security = {
            "network_policies": [],
            "ingress_controllers": [],
            "service_mesh": False,
            "mTLS": False,
            "recommendations": [],
        }

        # Generate default deny network policy
        network_security["network_policies"].append(
            {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "NetworkPolicy",
                "metadata": {"name": "default-deny-all", "namespace": "default"},
                "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
            }
        )

        # Generate recommendations
        network_security["recommendations"] = [
            "Implement network policies for all namespaces",
            "Use service mesh for advanced networking",
            "Enable mTLS for service-to-service communication",
            "Configure ingress controllers with TLS",
            "Monitor network traffic for anomalies",
            "Implement network segmentation",
        ]

        return network_security

    def _analyze_rbac_security(self, rbac_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze RBAC security configuration"""
        rbac_analysis = {"score": 0, "issues": [], "recommendations": []}

        # Check for overly permissive roles
        roles = rbac_config.get("roles", [])
        for role in roles:
            rules = role.get("rules", [])
            for rule in rules:
                if rule.get("verbs") == ["*"] or "*" in rule.get("resources", []):
                    rbac_analysis["issues"].append(
                        f"Overly permissive role: {role.get('metadata', {}).get('name')}"
                    )

        # Check for cluster-admin usage
        if rbac_config.get("cluster_admin_used", False):
            rbac_analysis["issues"].append("Cluster-admin role is being used")

        # Generate recommendations
        rbac_analysis["recommendations"] = [
            "Use least privilege principle",
            "Avoid cluster-admin role",
            "Implement role-based access control",
            "Regular RBAC audits",
            "Use service accounts for applications",
        ]

        return rbac_analysis

    def _analyze_network_security(
        self, network_policies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze network security policies"""
        network_analysis = {
            "score": 0,
            "policies_count": len(network_policies),
            "issues": [],
            "recommendations": [],
        }

        if not network_policies:
            network_analysis["issues"].append("No network policies configured")

        # Check for default deny policies
        has_default_deny = any(
            policy.get("metadata", {}).get("name") == "default-deny-all"
            for policy in network_policies
        )

        if not has_default_deny:
            network_analysis["issues"].append("Missing default deny network policy")

        network_analysis["recommendations"] = [
            "Implement default deny network policies",
            "Use network policies for all namespaces",
            "Configure ingress and egress rules",
            "Monitor network traffic",
        ]

        return network_analysis

    def _analyze_pod_security(self, pods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze pod security configuration"""
        pod_analysis = {
            "score": 0,
            "total_pods": len(pods),
            "secure_pods": 0,
            "issues": [],
            "recommendations": [],
        }

        for pod in pods:
            spec = pod.get("spec", {})
            security_context = spec.get("securityContext", {})

            # Check for security context
            if not security_context:
                pod_analysis["issues"].append(
                    f"Pod {pod.get('metadata', {}).get('name')} missing security context"
                )
            else:
                # Check for non-root user
                if security_context.get("runAsNonRoot"):
                    pod_analysis["secure_pods"] += 1
                else:
                    pod_analysis["issues"].append(
                        f"Pod {pod.get('metadata', {}).get('name')} running as root"
                    )

        pod_analysis["recommendations"] = [
            "Run pods as non-root user",
            "Use security contexts",
            "Implement pod security policies",
            "Use read-only root filesystem",
            "Drop unnecessary capabilities",
        ]

        return pod_analysis

    def _analyze_secrets_management(
        self, secrets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze secrets management"""
        secrets_analysis = {
            "score": 0,
            "total_secrets": len(secrets),
            "encrypted_secrets": 0,
            "issues": [],
            "recommendations": [],
        }

        for secret in secrets:
            # Check if secret is encrypted
            if secret.get("encrypted", False):
                secrets_analysis["encrypted_secrets"] += 1
            else:
                secrets_analysis["issues"].append(
                    f"Secret {secret.get('metadata', {}).get('name')} not encrypted"
                )

        secrets_analysis["recommendations"] = [
            "Enable encryption at rest",
            "Use external secrets management",
            "Implement secret rotation",
            "Audit secret access",
            "Use RBAC for secret access",
        ]

        return secrets_analysis

    def _scan_resource_vulnerabilities(
        self, resource: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Scan individual resource for vulnerabilities"""
        vulnerabilities = {"critical": [], "high": [], "medium": [], "low": []}

        resource_type = resource.get("kind", "")
        resource_name = resource.get("metadata", {}).get("name", "unknown")

        if resource_type == "Pod":
            # Check for privileged containers
            spec = resource.get("spec", {})
            containers = spec.get("containers", [])
            for container in containers:
                if container.get("securityContext", {}).get("privileged"):
                    vulnerabilities["critical"].append(
                        f"Privileged container in pod {resource_name}"
                    )

                # Check for host path mounts
                volume_mounts = container.get("volumeMounts", [])
                for mount in volume_mounts:
                    if mount.get("mountPath") == "/host":
                        vulnerabilities["high"].append(
                            f"Host path mount in pod {resource_name}"
                        )

        elif resource_type == "Service":
            # Check for overly permissive service
            spec = resource.get("spec", {})
            if spec.get("type") == "LoadBalancer" and not spec.get(
                "externalTrafficPolicy"
            ):
                vulnerabilities["medium"].append(
                    f"LoadBalancer service {resource_name} missing external traffic policy"
                )

        return vulnerabilities

    def _audit_cis_compliance(self, cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        """Audit CIS Kubernetes compliance"""
        cis_audit = {"passed_checks": [], "failed_checks": [], "warnings": []}

        # CIS Control 1: RBAC
        if cluster_config.get("rbac_enabled"):
            cis_audit["passed_checks"].append("1.1 RBAC is enabled")
        else:
            cis_audit["failed_checks"].append("1.1 RBAC is not enabled")

        # CIS Control 2: Network Policies
        if cluster_config.get("network_policies"):
            cis_audit["passed_checks"].append("2.1 Network policies are configured")
        else:
            cis_audit["failed_checks"].append("2.1 Network policies are not configured")

        # CIS Control 3: Pod Security
        if cluster_config.get("pod_security_policies"):
            cis_audit["passed_checks"].append(
                "3.1 Pod security policies are configured"
            )
        else:
            cis_audit["failed_checks"].append(
                "3.1 Pod security policies are not configured"
            )

        return cis_audit

    def _audit_nist_compliance(self, cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        """Audit NIST compliance"""
        nist_audit = {"passed_checks": [], "failed_checks": [], "warnings": []}

        # NIST AC-2: Account Management
        if cluster_config.get("service_accounts"):
            nist_audit["passed_checks"].append(
                "AC-2 Service accounts are properly managed"
            )
        else:
            nist_audit["failed_checks"].append(
                "AC-2 Service accounts are not properly managed"
            )

        return nist_audit

    def _audit_sox_compliance(self, cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        """Audit SOX compliance"""
        sox_audit = {"passed_checks": [], "failed_checks": [], "warnings": []}

        # SOX requires access controls
        if cluster_config.get("access_controls"):
            sox_audit["passed_checks"].append("Access controls are implemented")
        else:
            sox_audit["failed_checks"].append("Access controls are not implemented")

        return sox_audit

    def _analyze_event_threats(
        self, events: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Analyze cluster events for threats"""
        threats = {"critical": [], "high": [], "medium": [], "low": []}

        for event in events:
            event.get("type", "")
            reason = event.get("reason", "")
            message = event.get("message", "")

            # Check for suspicious events
            if "Unauthorized" in message or "Forbidden" in message:
                threats["high"].append(f"Unauthorized access attempt: {message}")

            if "Failed" in reason and "Create" in reason:
                threats["medium"].append(f"Failed resource creation: {message}")

        return threats

    def _analyze_log_threats(self, logs: List[str]) -> Dict[str, List[str]]:
        """Analyze logs for security threats"""
        threats = {"critical": [], "high": [], "medium": [], "low": []}

        for log in logs:
            # Check for suspicious patterns
            if "password" in log.lower() or "secret" in log.lower():
                threats["high"].append("Potential credential exposure in logs")

            if "error" in log.lower() and "authentication" in log.lower():
                threats["medium"].append("Authentication error detected")

        return threats

    def _detect_anomalies(
        self, events: List[Dict[str, Any]], logs: List[str]
    ) -> List[str]:
        """Detect anomalies in events and logs"""
        anomalies = []

        # Check for unusual event frequency
        event_counts = {}
        for event in events:
            event_type = event.get("type", "")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        for event_type, count in event_counts.items():
            if count > 100:  # Threshold for anomaly
                anomalies.append(f"Unusual frequency of {event_type} events: {count}")

        return anomalies

    def _create_network_policies(
        self, namespace: str, config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create network policies"""
        policies = []

        # Default deny policy
        policies.append(
            {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "NetworkPolicy",
                "metadata": {"name": "default-deny-all", "namespace": namespace},
                "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
            }
        )

        return policies

    def _create_pod_security_policies(
        self, namespace: str, config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create pod security policies"""
        policies = []

        # Restrictive PSP
        policies.append(
            {
                "apiVersion": "policy/v1beta1",
                "kind": "PodSecurityPolicy",
                "metadata": {"name": "restrictive-psp"},
                "spec": {
                    "privileged": False,
                    "allowPrivilegeEscalation": False,
                    "runAsUser": {"rule": "MustRunAsNonRoot"},
                },
            }
        )

        return policies

    def _create_rbac_policies(
        self, namespace: str, config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create RBAC policies"""
        policies = []

        # Service account
        policies.append(
            {
                "apiVersion": "v1",
                "kind": "ServiceAccount",
                "metadata": {"name": "restricted-sa", "namespace": namespace},
            }
        )

        return policies

    def _create_admission_controller_policies(
        self, namespace: str, config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create admission controller policies"""
        policies = []

        # Validating webhook
        policies.append(
            {
                "apiVersion": "admissionregistration.k8s.io/v1",
                "kind": "ValidatingWebhookConfiguration",
                "metadata": {"name": "security-webhook"},
                "webhooks": [
                    {
                        "name": "security.kubernetes.io",
                        "rules": [
                            {
                                "apiGroups": [""],
                                "apiVersions": ["v1"],
                                "operations": ["CREATE", "UPDATE"],
                                "resources": ["pods"],
                            }
                        ],
                    }
                ],
            }
        )

        return policies

    def _calculate_security_score(self, security_analysis: Dict[str, Any]) -> int:
        """Calculate overall security score"""
        score = 100

        # Deduct points for issues
        if security_analysis.get("rbac", {}).get("issues"):
            score -= 20

        if security_analysis.get("network", {}).get("issues"):
            score -= 20

        if security_analysis.get("pod_security", {}).get("issues"):
            score -= 20

        return max(0, score)

    def _determine_security_status(self, score: int) -> str:
        """Determine security status based on score"""
        if score >= 90:
            return "secure"
        elif score >= 70:
            return "moderate"
        else:
            return "insecure"

    def _determine_risk_level(self, security_analysis: Dict[str, Any]) -> str:
        """Determine risk level"""
        if security_analysis.get("vulnerabilities"):
            return "high"
        elif security_analysis.get("compliance_gaps"):
            return "medium"
        else:
            return "low"

    def _generate_security_recommendations(
        self, security_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate security recommendations"""
        recommendations = []

        if security_analysis.get("rbac", {}).get("issues"):
            recommendations.append("Implement proper RBAC with least privilege")

        if security_analysis.get("network", {}).get("issues"):
            recommendations.append("Configure network policies for all namespaces")

        if security_analysis.get("pod_security", {}).get("issues"):
            recommendations.append("Implement pod security policies")

        recommendations.extend(
            [
                "Enable audit logging",
                "Implement secrets management",
                "Regular security scans",
                "Monitor for threats",
                "Keep cluster updated",
            ]
        )

        return recommendations

    def _generate_vulnerability_recommendations(
        self, vulnerability_scan: Dict[str, Any]
    ) -> List[str]:
        """Generate vulnerability remediation recommendations"""
        recommendations = []

        if vulnerability_scan["critical_vulnerabilities"]:
            recommendations.append("Address critical vulnerabilities immediately")

        if vulnerability_scan["high_vulnerabilities"]:
            recommendations.append("Fix high severity vulnerabilities")

        recommendations.extend(
            [
                "Implement security scanning in CI/CD",
                "Use vulnerability scanning tools",
                "Keep images updated",
                "Implement image signing",
            ]
        )

        return recommendations

    def _generate_threat_recommendations(
        self, threat_detection: Dict[str, Any]
    ) -> List[str]:
        """Generate threat response recommendations"""
        recommendations = []

        if threat_detection["critical_threats"]:
            recommendations.append("Respond to critical threats immediately")

        if threat_detection["high_threats"]:
            recommendations.append("Investigate high priority threats")

        recommendations.extend(
            [
                "Implement threat detection tools",
                "Set up security monitoring",
                "Create incident response plan",
                "Regular security training",
            ]
        )

        return recommendations


# Global instance
cks_security = CKSSecurity()
