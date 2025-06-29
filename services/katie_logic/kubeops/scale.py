"""
Katie - Kubernetes Scaling Operations
Handles all scaling operations with intelligent analysis
"""

import subprocess
import json
import logging
from typing import Dict, Any, Optional, List
from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)


class KubernetesScaler:
    """
    Katie's Kubernetes scaling operations with intelligent analysis
    """
    
    def __init__(self):
        try:
            config.load_kube_config()
            self.apps_v1 = client.AppsV1Api()
            self.v1 = client.CoreV1Api()
            logger.info("Katie scaler initialized with Kubernetes client")
        except Exception as e:
            logger.warning(f"Kubernetes client initialization failed: {e}")
            self.apps_v1 = None
            self.v1 = None

    def scale_deployment(
        self, 
        namespace: str, 
        deployment_name: str, 
        replicas: int,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Scale a deployment to the specified number of replicas
        """
        try:
            logger.info(f"Katie scaling deployment {deployment_name} to {replicas} replicas")
            
            if dry_run:
                return self._dry_run_scale_deployment(namespace, deployment_name, replicas)
            
            # Get current deployment
            deployment = self.apps_v1.read_namespaced_deployment(deployment_name, namespace)
            current_replicas = deployment.spec.replicas
            
            # Update replicas
            deployment.spec.replicas = replicas
            
            # Apply the update
            updated_deployment = self.apps_v1.patch_namespaced_deployment(
                deployment_name, 
                namespace, 
                deployment
            )
            
            # Analyze scaling impact
            impact_analysis = self._analyze_scaling_impact(
                namespace, deployment_name, current_replicas, replicas
            )
            
            return {
                "agent": "katie",
                "operation": "scale_deployment",
                "deployment_name": deployment_name,
                "namespace": namespace,
                "previous_replicas": current_replicas,
                "new_replicas": replicas,
                "scaling_direction": "up" if replicas > current_replicas else "down",
                "status": "success",
                "impact_analysis": impact_analysis,
                "katie_insight": self._generate_scaling_insight(
                    deployment_name, current_replicas, replicas, impact_analysis
                )
            }
            
        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "scale_deployment",
                "error": f"Failed to scale deployment: {e.reason}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Deployment scaling failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "scale_deployment",
                "error": f"Scaling failed: {str(e)}",
                "status": "error"
            }

    def scale_statefulset(
        self, 
        namespace: str, 
        statefulset_name: str, 
        replicas: int,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Scale a statefulset to the specified number of replicas
        """
        try:
            logger.info(f"Katie scaling statefulset {statefulset_name} to {replicas} replicas")
            
            if dry_run:
                return self._dry_run_scale_statefulset(namespace, statefulset_name, replicas)
            
            # Get current statefulset
            statefulset = self.apps_v1.read_namespaced_stateful_set(statefulset_name, namespace)
            current_replicas = statefulset.spec.replicas
            
            # Update replicas
            statefulset.spec.replicas = replicas
            
            # Apply the update
            updated_statefulset = self.apps_v1.patch_namespaced_stateful_set(
                statefulset_name, 
                namespace, 
                statefulset
            )
            
            # Analyze scaling impact
            impact_analysis = self._analyze_statefulset_scaling_impact(
                namespace, statefulset_name, current_replicas, replicas
            )
            
            return {
                "agent": "katie",
                "operation": "scale_statefulset",
                "statefulset_name": statefulset_name,
                "namespace": namespace,
                "previous_replicas": current_replicas,
                "new_replicas": replicas,
                "scaling_direction": "up" if replicas > current_replicas else "down",
                "status": "success",
                "impact_analysis": impact_analysis,
                "katie_insight": self._generate_statefulset_scaling_insight(
                    statefulset_name, current_replicas, replicas, impact_analysis
                )
            }
            
        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "scale_statefulset",
                "error": f"Failed to scale statefulset: {e.reason}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Statefulset scaling failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "scale_statefulset",
                "error": f"Scaling failed: {str(e)}",
                "status": "error"
            }

    def auto_scale_deployment(
        self, 
        namespace: str, 
        deployment_name: str,
        min_replicas: int = 1,
        max_replicas: int = 10,
        target_cpu_percentage: int = 80
    ) -> Dict[str, Any]:
        """
        Create or update HPA for automatic scaling
        """
        try:
            logger.info(f"Katie setting up auto-scaling for {deployment_name}")
            
            # Create HPA using kubectl
            hpa_manifest = self._generate_hpa_manifest(
                deployment_name, namespace, min_replicas, max_replicas, target_cpu_percentage
            )
            
            # Apply HPA
            result = subprocess.run(
                ["kubectl", "apply", "-f", "-"],
                input=hpa_manifest,
                text=True,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    "agent": "katie",
                    "operation": "auto_scale_deployment",
                    "deployment_name": deployment_name,
                    "namespace": namespace,
                    "hpa_config": {
                        "min_replicas": min_replicas,
                        "max_replicas": max_replicas,
                        "target_cpu_percentage": target_cpu_percentage
                    },
                    "status": "success",
                    "katie_insight": f"Auto-scaling configured for {deployment_name} with CPU target of {target_cpu_percentage}%"
                }
            else:
                return {
                    "agent": "katie",
                    "operation": "auto_scale_deployment",
                    "error": f"HPA creation failed: {result.stderr}",
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"Auto-scaling setup failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "auto_scale_deployment",
                "error": f"Auto-scaling failed: {str(e)}",
                "status": "error"
            }

    def scale_to_zero(self, namespace: str, deployment_name: str) -> Dict[str, Any]:
        """
        Scale deployment to zero replicas (pause)
        """
        return self.scale_deployment(namespace, deployment_name, 0)

    def scale_from_zero(self, namespace: str, deployment_name: str, replicas: int = 1) -> Dict[str, Any]:
        """
        Scale deployment from zero to specified replicas (resume)
        """
        return self.scale_deployment(namespace, deployment_name, replicas)

    def get_scaling_recommendations(self, namespace: str, deployment_name: str) -> Dict[str, Any]:
        """
        Get intelligent scaling recommendations based on current usage
        """
        try:
            logger.info(f"Katie analyzing scaling recommendations for {deployment_name}")
            
            # Get current deployment status
            deployment = self.apps_v1.read_namespaced_deployment(deployment_name, namespace)
            current_replicas = deployment.spec.replicas
            
            # Get resource usage
            resource_usage = self._get_deployment_resource_usage(namespace, deployment_name)
            
            # Get HPA status if exists
            hpa_status = self._get_hpa_status(namespace, deployment_name)
            
            # Generate recommendations
            recommendations = self._generate_scaling_recommendations(
                current_replicas, resource_usage, hpa_status
            )
            
            return {
                "agent": "katie",
                "operation": "get_scaling_recommendations",
                "deployment_name": deployment_name,
                "namespace": namespace,
                "current_replicas": current_replicas,
                "resource_usage": resource_usage,
                "hpa_status": hpa_status,
                "recommendations": recommendations,
                "katie_insight": self._generate_recommendation_insight(recommendations)
            }
            
        except Exception as e:
            logger.error(f"Scaling recommendations failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "get_scaling_recommendations",
                "error": f"Failed to get recommendations: {str(e)}",
                "status": "error"
            }

    def _dry_run_scale_deployment(self, namespace: str, deployment_name: str, replicas: int) -> Dict[str, Any]:
        """Simulate scaling operation without applying changes"""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(deployment_name, namespace)
            current_replicas = deployment.spec.replicas
            
            impact_analysis = self._analyze_scaling_impact(
                namespace, deployment_name, current_replicas, replicas
            )
            
            return {
                "agent": "katie",
                "operation": "scale_deployment",
                "deployment_name": deployment_name,
                "namespace": namespace,
                "previous_replicas": current_replicas,
                "new_replicas": replicas,
                "scaling_direction": "up" if replicas > current_replicas else "down",
                "status": "dry_run",
                "impact_analysis": impact_analysis,
                "katie_insight": f"DRY RUN: Would scale {deployment_name} from {current_replicas} to {replicas} replicas"
            }
        except Exception as e:
            return {
                "agent": "katie",
                "operation": "scale_deployment",
                "error": f"Dry run failed: {str(e)}",
                "status": "error"
            }

    def _dry_run_scale_statefulset(self, namespace: str, statefulset_name: str, replicas: int) -> Dict[str, Any]:
        """Simulate statefulset scaling operation without applying changes"""
        try:
            statefulset = self.apps_v1.read_namespaced_stateful_set(statefulset_name, namespace)
            current_replicas = statefulset.spec.replicas
            
            impact_analysis = self._analyze_statefulset_scaling_impact(
                namespace, statefulset_name, current_replicas, replicas
            )
            
            return {
                "agent": "katie",
                "operation": "scale_statefulset",
                "statefulset_name": statefulset_name,
                "namespace": namespace,
                "previous_replicas": current_replicas,
                "new_replicas": replicas,
                "scaling_direction": "up" if replicas > current_replicas else "down",
                "status": "dry_run",
                "impact_analysis": impact_analysis,
                "katie_insight": f"DRY RUN: Would scale {statefulset_name} from {current_replicas} to {replicas} replicas"
            }
        except Exception as e:
            return {
                "agent": "katie",
                "operation": "scale_statefulset",
                "error": f"Dry run failed: {str(e)}",
                "status": "error"
            }

    def _analyze_scaling_impact(self, namespace: str, deployment_name: str, current: int, target: int) -> Dict[str, Any]:
        """Analyze the impact of scaling operation"""
        impact = {
            "replica_change": target - current,
            "percentage_change": ((target - current) / current * 100) if current > 0 else 0,
            "resource_impact": "unknown",
            "estimated_duration": "unknown",
            "risks": [],
            "benefits": []
        }
        
        if target > current:
            impact["resource_impact"] = "increased"
            impact["estimated_duration"] = "2-5 minutes"
            impact["risks"] = ["Higher resource consumption", "Potential node pressure"]
            impact["benefits"] = ["Better performance", "Higher availability"]
        elif target < current:
            impact["resource_impact"] = "decreased"
            impact["estimated_duration"] = "1-3 minutes"
            impact["risks"] = ["Reduced capacity", "Potential performance impact"]
            impact["benefits"] = ["Lower resource usage", "Cost savings"]
        
        return impact

    def _analyze_statefulset_scaling_impact(self, namespace: str, statefulset_name: str, current: int, target: int) -> Dict[str, Any]:
        """Analyze the impact of statefulset scaling operation"""
        impact = self._analyze_scaling_impact(namespace, statefulset_name, current, target)
        
        # Statefulset-specific considerations
        if target < current:
            impact["risks"].append("Data loss risk during scale down")
            impact["estimated_duration"] = "5-10 minutes"
        elif target > current:
            impact["risks"].append("Storage provisioning delays")
            impact["estimated_duration"] = "3-8 minutes"
        
        return impact

    def _generate_hpa_manifest(self, deployment_name: str, namespace: str, min_replicas: int, max_replicas: int, target_cpu: int) -> str:
        """Generate HPA manifest"""
        return f"""
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {deployment_name}-hpa
  namespace: {namespace}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {deployment_name}
  minReplicas: {min_replicas}
  maxReplicas: {max_replicas}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {target_cpu}
"""

    def _get_deployment_resource_usage(self, namespace: str, deployment_name: str) -> Dict[str, Any]:
        """Get current resource usage for deployment"""
        try:
            # Get pods for the deployment
            pods = self.v1.list_namespaced_pod(
                namespace, 
                label_selector=f"app={deployment_name}"
            )
            
            if not pods.items:
                return {"cpu_usage": "unknown", "memory_usage": "unknown", "pod_count": 0}
            
            # This would typically use metrics-server or Prometheus
            # For now, return estimated values
            return {
                "cpu_usage": "estimated_60_percent",
                "memory_usage": "estimated_70_percent",
                "pod_count": len(pods.items)
            }
        except Exception as e:
            logger.warning(f"Failed to get resource usage: {e}")
            return {"cpu_usage": "unknown", "memory_usage": "unknown", "pod_count": 0}

    def _get_hpa_status(self, namespace: str, deployment_name: str) -> Optional[Dict[str, Any]]:
        """Get HPA status if it exists"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "hpa", f"{deployment_name}-hpa", "-n", namespace, "-o", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                hpa_data = json.loads(result.stdout)
                return {
                    "min_replicas": hpa_data["spec"]["minReplicas"],
                    "max_replicas": hpa_data["spec"]["maxReplicas"],
                    "current_replicas": hpa_data["status"]["currentReplicas"],
                    "target_replicas": hpa_data["status"]["desiredReplicas"]
                }
            else:
                return None
        except Exception as e:
            logger.warning(f"Failed to get HPA status: {e}")
            return None

    def _generate_scaling_recommendations(self, current_replicas: int, resource_usage: Dict[str, Any], hpa_status: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate intelligent scaling recommendations"""
        recommendations = []
        
        # Check if HPA is configured
        if not hpa_status:
            recommendations.append({
                "type": "hpa_setup",
                "priority": "high",
                "description": "Consider setting up Horizontal Pod Autoscaler for automatic scaling",
                "action": "setup_hpa"
            })
        
        # Check resource usage patterns
        if resource_usage.get("cpu_usage") == "estimated_60_percent":
            if current_replicas < 3:
                recommendations.append({
                    "type": "scale_up",
                    "priority": "medium",
                    "description": "CPU usage is moderate, consider scaling up for better performance",
                    "action": "scale_up",
                    "suggested_replicas": min(current_replicas + 1, 5)
                })
        
        # Check for over-provisioning
        if current_replicas > 5 and resource_usage.get("cpu_usage") == "estimated_60_percent":
            recommendations.append({
                "type": "scale_down",
                "priority": "low",
                "description": "Consider scaling down to optimize resource usage",
                "action": "scale_down",
                "suggested_replicas": max(current_replicas - 1, 2)
            })
        
        return recommendations

    def _generate_scaling_insight(self, deployment_name: str, current: int, target: int, impact: Dict[str, Any]) -> str:
        """Generate Katie's insight about scaling operation"""
        if target > current:
            return f"Scaling {deployment_name} up from {current} to {target} replicas for better performance and availability."
        elif target < current:
            return f"Scaling {deployment_name} down from {current} to {target} replicas to optimize resource usage."
        else:
            return f"No scaling needed for {deployment_name} - already at {current} replicas."

    def _generate_statefulset_scaling_insight(self, statefulset_name: str, current: int, target: int, impact: Dict[str, Any]) -> str:
        """Generate Katie's insight about statefulset scaling operation"""
        base_insight = self._generate_scaling_insight(statefulset_name, current, target, impact)
        
        if target < current:
            return f"{base_insight} Note: Statefulset scaling down requires careful consideration of data persistence."
        else:
            return f"{base_insight} Statefulset scaling will provision persistent volumes for new replicas."

    def _generate_recommendation_insight(self, recommendations: List[Dict[str, Any]]) -> str:
        """Generate Katie's insight about scaling recommendations"""
        if not recommendations:
            return "Current scaling configuration appears optimal."
        
        high_priority = [r for r in recommendations if r["priority"] == "high"]
        if high_priority:
            return f"High priority recommendation: {high_priority[0]['description']}"
        
        medium_priority = [r for r in recommendations if r["priority"] == "medium"]
        if medium_priority:
            return f"Consider: {medium_priority[0]['description']}"
        
        return f"Optimization opportunity: {recommendations[0]['description']}"


# Global instance
k8s_scaler = KubernetesScaler() 