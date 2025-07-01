"""
Katie - Kubernetes Describe Operations
Handles all describe operations for Kubernetes resources
"""

import subprocess
import json
import logging
from typing import Dict, Any, List, Optional
from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)


class KubernetesDescriber:
    """
    Katie's Kubernetes resource describer with intelligent analysis
    """

    def __init__(self):
        try:
            # Load kubeconfig
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.networking_v1 = client.NetworkingV1Api()
            self.rbac_v1 = client.RbacAuthorizationV1Api()
            logger.info("Katie initialized with Kubernetes client")
        except Exception as e:
            logger.warning(f"Kubernetes client initialization failed: {e}")
            self.v1 = None
            self.apps_v1 = None
            self.networking_v1 = None
            self.rbac_v1 = None

    def describe_pod(self, namespace: str, pod_name: str) -> Dict[str, Any]:
        """
        Describe a specific pod with detailed analysis
        """
        try:
            logger.info(f"Katie describing pod: {pod_name} in {namespace}")

            # Get pod details
            pod = self.v1.read_namespaced_pod(pod_name, namespace)

            # Analyze pod status
            status_analysis = self._analyze_pod_status(pod)

            # Get pod logs (last 50 lines)
            logs = self._get_pod_logs(namespace, pod_name, tail_lines=50)

            # Analyze resource usage
            resource_analysis = self._analyze_pod_resources(pod)

            return {
                "agent": "katie",
                "operation": "describe_pod",
                "pod_name": pod_name,
                "namespace": namespace,
                "status": pod.status.phase,
                "status_analysis": status_analysis,
                "resource_analysis": resource_analysis,
                "recent_logs": logs,
                "containers": self._extract_container_info(pod),
                "events": self._get_pod_events(namespace, pod_name),
                "katie_insight": self._generate_katie_insight(pod, status_analysis),
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "describe_pod",
                "error": f"Pod {pod_name} not found or inaccessible: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Pod description failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "describe_pod",
                "error": f"Failed to describe pod: {str(e)}",
                "status": "error",
            }

    def describe_deployment(
        self, namespace: str, deployment_name: str
    ) -> Dict[str, Any]:
        """
        Describe a deployment with scaling and rollout analysis
        """
        try:
            logger.info(
                f"Katie describing deployment: {deployment_name} in {namespace}"
            )

            # Get deployment details
            deployment = self.apps_v1.read_namespaced_deployment(
                deployment_name, namespace
            )

            # Get associated pods
            pods = self._get_deployment_pods(namespace, deployment_name)

            # Analyze deployment status
            status_analysis = self._analyze_deployment_status(deployment, pods)

            # Get rollout history
            rollout_history = self._get_rollout_history(deployment_name, namespace)

            return {
                "agent": "katie",
                "operation": "describe_deployment",
                "deployment_name": deployment_name,
                "namespace": namespace,
                "replicas": {
                    "desired": deployment.spec.replicas,
                    "current": deployment.status.replicas,
                    "ready": deployment.status.ready_replicas,
                    "available": deployment.status.available_replicas,
                },
                "status_analysis": status_analysis,
                "rollout_history": rollout_history,
                "pods": pods,
                "strategy": (
                    deployment.spec.strategy.type
                    if deployment.spec.strategy
                    else "RollingUpdate"
                ),
                "katie_insight": self._generate_deployment_insight(
                    deployment, status_analysis
                ),
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "describe_deployment",
                "error": f"Deployment {deployment_name} not found: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Deployment description failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "describe_deployment",
                "error": f"Failed to describe deployment: {str(e)}",
                "status": "error",
            }

    def describe_service(self, namespace: str, service_name: str) -> Dict[str, Any]:
        """
        Describe a service with networking analysis
        """
        try:
            logger.info(f"Katie describing service: {service_name} in {namespace}")

            # Get service details
            service = self.v1.read_namespaced_service(service_name, namespace)

            # Get endpoints
            endpoints = self._get_service_endpoints(namespace, service_name)

            # Analyze service configuration
            config_analysis = self._analyze_service_config(service)

            return {
                "agent": "katie",
                "operation": "describe_service",
                "service_name": service_name,
                "namespace": namespace,
                "type": service.spec.type,
                "cluster_ip": service.spec.cluster_ip,
                "external_ip": service.spec.external_ips,
                "ports": self._extract_service_ports(service),
                "endpoints": endpoints,
                "config_analysis": config_analysis,
                "katie_insight": self._generate_service_insight(service, endpoints),
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "describe_service",
                "error": f"Service {service_name} not found: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Service description failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "describe_service",
                "error": f"Failed to describe service: {str(e)}",
                "status": "error",
            }

    def describe_namespace(self, namespace: str) -> Dict[str, Any]:
        """
        Describe a namespace with resource overview
        """
        try:
            logger.info(f"Katie describing namespace: {namespace}")

            # Get namespace details
            ns = self.v1.read_namespace(namespace)

            # Get resource counts
            resource_counts = self._get_namespace_resources(namespace)

            # Get namespace events
            events = self._get_namespace_events(namespace)

            return {
                "agent": "katie",
                "operation": "describe_namespace",
                "namespace": namespace,
                "status": ns.status.phase,
                "resource_counts": resource_counts,
                "events": events,
                "labels": ns.metadata.labels,
                "annotations": ns.metadata.annotations,
                "katie_insight": self._generate_namespace_insight(ns, resource_counts),
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "describe_namespace",
                "error": f"Namespace {namespace} not found: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Namespace description failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "describe_namespace",
                "error": f"Failed to describe namespace: {str(e)}",
                "status": "error",
            }

    def describe_all_pods(self, namespace: str = "default") -> Dict[str, Any]:
        """
        Describe all pods in a namespace with summary analysis
        """
        try:
            logger.info(f"Katie describing all pods in namespace: {namespace}")

            # Get all pods
            pods = self.v1.list_namespaced_pod(namespace)

            # Analyze pod statuses
            status_summary = self._analyze_pod_status_summary(pods.items)

            # Get resource usage summary
            resource_summary = self._analyze_resource_summary(pods.items)

            return {
                "agent": "katie",
                "operation": "describe_all_pods",
                "namespace": namespace,
                "total_pods": len(pods.items),
                "status_summary": status_summary,
                "resource_summary": resource_summary,
                "pods": [self._extract_pod_summary(pod) for pod in pods.items],
                "katie_insight": self._generate_pod_summary_insight(
                    status_summary, resource_summary
                ),
            }

        except Exception as e:
            logger.error(f"Pod summary description failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "describe_all_pods",
                "error": f"Failed to describe pods: {str(e)}",
                "status": "error",
            }

    def _analyze_pod_status(self, pod) -> Dict[str, Any]:
        """Analyze pod status and provide insights"""
        status = pod.status.phase

        analysis = {
            "status": status,
            "healthy": status == "Running",
            "issues": [],
            "recommendations": [],
        }

        # Check for common issues
        if status == "Pending":
            analysis["issues"].append("Pod is pending - check resource availability")
            analysis["recommendations"].append("Verify node resources and scheduling")
        elif status == "Failed":
            analysis["issues"].append("Pod has failed - check container logs")
            analysis["recommendations"].append("Review recent logs for error details")
        elif status == "Unknown":
            analysis["issues"].append("Pod status unknown - check node connectivity")
            analysis["recommendations"].append("Verify node health and network")

        # Check container statuses
        if pod.status.container_statuses:
            for container in pod.status.container_statuses:
                if not container.ready:
                    analysis["issues"].append(f"Container {container.name} not ready")
                    analysis["recommendations"].append(
                        f"Check logs for container {container.name}"
                    )

        return analysis

    def _get_pod_logs(
        self, namespace: str, pod_name: str, tail_lines: int = 50
    ) -> List[str]:
        """Get recent pod logs"""
        try:
            logs = self.v1.read_namespaced_pod_log(
                pod_name, namespace, tail_lines=tail_lines
            )
            return logs.split("\n") if logs else []
        except Exception as e:
            logger.warning(f"Failed to get logs for {pod_name}: {e}")
            return []

    def _analyze_pod_resources(self, pod) -> Dict[str, Any]:
        """Analyze pod resource requests and limits"""
        containers = pod.spec.containers if pod.spec.containers else []

        total_requests = {"cpu": "0", "memory": "0"}
        total_limits = {"cpu": "0", "memory": "0"}

        for container in containers:
            if container.resources.requests:
                for resource, value in container.resources.requests.items():
                    if resource in total_requests:
                        # Simple addition (in real implementation, parse units)
                        total_requests[resource] = str(
                            int(total_requests[resource])
                            + int(str(value).replace("m", ""))
                        )

            if container.resources.limits:
                for resource, value in container.resources.limits.items():
                    if resource in total_limits:
                        total_limits[resource] = str(
                            int(total_limits[resource])
                            + int(str(value).replace("m", ""))
                        )

        return {
            "requests": total_requests,
            "limits": total_limits,
            "containers": len(containers),
        }

    def _extract_container_info(self, pod) -> List[Dict[str, Any]]:
        """Extract container information from pod"""
        containers = []
        if pod.status.container_statuses:
            for container in pod.status.container_statuses:
                containers.append(
                    {
                        "name": container.name,
                        "ready": container.ready,
                        "restart_count": container.restart_count,
                        "state": container.state.type if container.state else "Unknown",
                    }
                )
        return containers

    def _get_pod_events(self, namespace: str, pod_name: str) -> List[Dict[str, Any]]:
        """Get recent events for a pod"""
        try:
            events = self.v1.list_namespaced_event(
                namespace, field_selector=f"involvedObject.name={pod_name}"
            )
            return [
                {
                    "type": event.type,
                    "reason": event.reason,
                    "message": event.message,
                    "last_timestamp": (
                        event.last_timestamp.isoformat()
                        if event.last_timestamp
                        else None
                    ),
                }
                for event in events.items[:10]  # Last 10 events
            ]
        except Exception as e:
            logger.warning(f"Failed to get events for {pod_name}: {e}")
            return []

    def _generate_katie_insight(self, pod, status_analysis: Dict[str, Any]) -> str:
        """Generate Katie's insight about the pod"""
        if status_analysis["healthy"]:
            return f"Pod {pod.metadata.name} is healthy and running smoothly."
        else:
            issues = status_analysis["issues"]
            if issues:
                return f"Pod {pod.metadata.name} has issues: {'; '.join(issues[:2])}"
            else:
                return f"Pod {pod.metadata.name} status: {pod.status.phase}"

    def _analyze_deployment_status(
        self, deployment, pods: List[Dict]
    ) -> Dict[str, Any]:
        """Analyze deployment status and health"""
        desired = deployment.spec.replicas
        current = deployment.status.replicas
        ready = deployment.status.ready_replicas

        analysis = {
            "healthy": ready == desired,
            "scaling": current != desired,
            "issues": [],
            "recommendations": [],
        }

        if ready < desired:
            analysis["issues"].append(f"Only {ready}/{desired} replicas are ready")
            analysis["recommendations"].append(
                "Check pod logs and events for failed replicas"
            )

        if current != desired:
            analysis["issues"].append(
                f"Scaling in progress: {current}/{desired} replicas"
            )
            analysis["recommendations"].append("Monitor scaling progress")

        return analysis

    def _get_deployment_pods(
        self, namespace: str, deployment_name: str
    ) -> List[Dict[str, Any]]:
        """Get pods associated with a deployment"""
        try:
            pods = self.v1.list_namespaced_pod(
                namespace, label_selector=f"app={deployment_name}"
            )
            return [
                {
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "ready": (
                        pod.status.ready_replicas
                        if hasattr(pod.status, "ready_replicas")
                        else None
                    ),
                }
                for pod in pods.items
            ]
        except Exception as e:
            logger.warning(f"Failed to get deployment pods: {e}")
            return []

    def _get_rollout_history(
        self, deployment_name: str, namespace: str
    ) -> List[Dict[str, Any]]:
        """Get deployment rollout history using kubectl"""
        try:
            result = subprocess.run(
                [
                    "kubectl",
                    "rollout",
                    "history",
                    f"deployment/{deployment_name}",
                    "-n",
                    namespace,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                history = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            history.append(
                                {
                                    "revision": parts[0],
                                    "change_cause": (
                                        " ".join(parts[1:])
                                        if len(parts) > 1
                                        else "No change cause"
                                    ),
                                }
                            )
                return history
            else:
                return []
        except Exception as e:
            logger.warning(f"Failed to get rollout history: {e}")
            return []

    def _generate_deployment_insight(
        self, deployment, status_analysis: Dict[str, Any]
    ) -> str:
        """Generate Katie's insight about the deployment"""
        if status_analysis["healthy"]:
            return f"Deployment {deployment.metadata.name} is healthy with all replicas ready."
        else:
            issues = status_analysis["issues"]
            if issues:
                return f"Deployment {deployment.metadata.name} needs attention: {'; '.join(issues[:2])}"
            else:
                return f"Deployment {deployment.metadata.name} status: {deployment.status.phase}"

    def _analyze_service_config(self, service) -> Dict[str, Any]:
        """Analyze service configuration"""
        return {
            "type": service.spec.type,
            "has_external_ip": bool(service.spec.external_ips),
            "load_balancer": service.spec.type == "LoadBalancer",
            "node_port": service.spec.type == "NodePort",
            "cluster_internal": service.spec.type == "ClusterIP",
        }

    def _extract_service_ports(self, service) -> List[Dict[str, Any]]:
        """Extract service port information"""
        ports = []
        if service.spec.ports:
            for port in service.spec.ports:
                ports.append(
                    {
                        "name": port.name,
                        "port": port.port,
                        "target_port": port.target_port,
                        "protocol": port.protocol,
                    }
                )
        return ports

    def _get_service_endpoints(
        self, namespace: str, service_name: str
    ) -> List[Dict[str, Any]]:
        """Get service endpoints"""
        try:
            endpoints = self.v1.read_namespaced_endpoints(service_name, namespace)
            return [
                {
                    "addresses": (
                        [addr.ip for addr in subset.addresses]
                        if subset.addresses
                        else []
                    ),
                    "ports": (
                        [port.port for port in subset.ports] if subset.ports else []
                    ),
                }
                for subset in endpoints.subsets
            ]
        except Exception as e:
            logger.warning(f"Failed to get service endpoints: {e}")
            return []

    def _generate_service_insight(self, service, endpoints: List[Dict]) -> str:
        """Generate Katie's insight about the service"""
        if not endpoints:
            return f"Service {service.metadata.name} has no endpoints - check pod selectors."
        else:
            total_endpoints = sum(len(ep["addresses"]) for ep in endpoints)
            return f"Service {service.metadata.name} is healthy with {total_endpoints} endpoints."

    def _get_namespace_resources(self, namespace: str) -> Dict[str, int]:
        """Get resource counts for a namespace"""
        try:
            pods = len(self.v1.list_namespaced_pod(namespace).items)
            services = len(self.v1.list_namespaced_service(namespace).items)
            deployments = len(self.apps_v1.list_namespaced_deployment(namespace).items)

            return {"pods": pods, "services": services, "deployments": deployments}
        except Exception as e:
            logger.warning(f"Failed to get namespace resources: {e}")
            return {"pods": 0, "services": 0, "deployments": 0}

    def _get_namespace_events(self, namespace: str) -> List[Dict[str, Any]]:
        """Get recent namespace events"""
        try:
            events = self.v1.list_namespaced_event(namespace)
            return [
                {
                    "type": event.type,
                    "reason": event.reason,
                    "message": event.message,
                    "last_timestamp": (
                        event.last_timestamp.isoformat()
                        if event.last_timestamp
                        else None
                    ),
                }
                for event in events.items[:10]  # Last 10 events
            ]
        except Exception as e:
            logger.warning(f"Failed to get namespace events: {e}")
            return []

    def _generate_namespace_insight(self, ns, resource_counts: Dict[str, int]) -> str:
        """Generate Katie's insight about the namespace"""
        total_resources = sum(resource_counts.values())
        if total_resources == 0:
            return f"Namespace {ns.metadata.name} is empty - ready for deployments."
        else:
            return f"Namespace {ns.metadata.name} contains {total_resources} resources and is active."

    def _analyze_pod_status_summary(self, pods: List) -> Dict[str, int]:
        """Analyze pod status summary"""
        status_counts = {}
        for pod in pods:
            status = pod.status.phase
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts

    def _analyze_resource_summary(self, pods: List) -> Dict[str, Any]:
        """Analyze resource usage summary"""
        total_pods = len(pods)
        running_pods = len([p for p in pods if p.status.phase == "Running"])

        return {
            "total": total_pods,
            "running": running_pods,
            "healthy_percentage": (
                (running_pods / total_pods * 100) if total_pods > 0 else 0
            ),
        }

    def _extract_pod_summary(self, pod) -> Dict[str, Any]:
        """Extract summary information from a pod"""
        return {
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "ready": (
                pod.status.ready_replicas
                if hasattr(pod.status, "ready_replicas")
                else None
            ),
            "restarts": (
                sum(
                    container.restart_count
                    for container in pod.status.container_statuses
                )
                if pod.status.container_statuses
                else 0
            ),
        }

    def _generate_pod_summary_insight(
        self, status_summary: Dict[str, int], resource_summary: Dict[str, Any]
    ) -> str:
        """Generate Katie's insight about pod summary"""
        running = status_summary.get("Running", 0)
        total = resource_summary["total"]

        if total == 0:
            return "No pods found in the namespace."
        elif running == total:
            return f"All {total} pods are running and healthy."
        else:
            failed = total - running
            return f"{running}/{total} pods are running. {failed} pods need attention."


# Global instance
k8s_describer = KubernetesDescriber()
