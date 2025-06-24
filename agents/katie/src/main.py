from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging

app = FastAPI(title="Katie Agent - Kubernetes Specialist")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentTaskInput(BaseModel):
    task_text: str
    context: Optional[Dict[str, Any]] = None
    cluster_info: Optional[Dict[str, Any]] = None

class KatieResponse(BaseModel):
    agent: str = "katie"
    task: str
    response: str
    kubernetes_solution: Dict[str, Any]
    generated_yaml: List[str]
    security_recommendations: List[str]
    confidence_score: float

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "katie",
        "specialization": "Kubernetes Operations & Security",
        "capabilities": [
            "Kubernetes Cluster Management",
            "CKA/CKS Certification Logic",
            "Security Scanning & Compliance",
            "Container Orchestration",
            "K8sGPT Integration",
            "Multi-Cluster Operations",
            "Performance Optimization",
            "Troubleshooting & Debugging"
        ]
    }

@app.post("/execute")
def execute(data: AgentTaskInput):
    """
    Katie specializes in Kubernetes operations and security
    - Manages Kubernetes clusters and deployments
    - Implements security best practices (CKS)
    - Integrates with K8sGPT for intelligent operations
    - Provides container orchestration solutions
    """
    try:
        logger.info(f"Katie processing Kubernetes task: {data.task_text}")
        
        # Analyze task for Kubernetes components
        k8s_components = _analyze_k8s_components(data.task_text)
        
        # Generate Kubernetes solution
        k8s_solution = _generate_k8s_solution(data.task_text, k8s_components)
        
        # Generate YAML manifests
        generated_yaml = _generate_yaml_manifests(data.task_text, k8s_components)
        
        # Security recommendations
        security_recommendations = _generate_security_recommendations(data.task_text, k8s_components)
        
        # Create response
        response = KatieResponse(
            task=data.task_text,
            response=_generate_k8s_response(data.task_text, k8s_components),
            kubernetes_solution=k8s_solution,
            generated_yaml=generated_yaml,
            security_recommendations=security_recommendations,
            confidence_score=_calculate_confidence(k8s_components)
        )
        
        logger.info(f"Katie completed task with {len(generated_yaml)} YAML manifests")
        return response
        
    except Exception as e:
        logger.error(f"Katie execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Katie execution failed: {str(e)}")

@app.post("/k8sgpt/analyze")
def k8sgpt_analyze(cluster_info: Dict[str, Any]):
    """
    Integrate with K8sGPT for intelligent cluster analysis
    """
    try:
        logger.info("Katie using K8sGPT for cluster analysis")
        
        # Simulate K8sGPT analysis
        analysis = _simulate_k8sgpt_analysis(cluster_info)
        
        return {
            "status": "analysis_complete",
            "k8sgpt_insights": analysis["insights"],
            "recommendations": analysis["recommendations"],
            "security_issues": analysis["security_issues"],
            "performance_optimizations": analysis["performance_optimizations"]
        }
        
    except Exception as e:
        logger.error(f"K8sGPT analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"K8sGPT analysis failed: {str(e)}")

@app.get("/capabilities")
def get_capabilities():
    """Get current Katie capabilities"""
    return {
        "agent": "katie",
        "specialization": "Kubernetes Operations & Security",
        "current_capabilities": [
            "Kubernetes Cluster Management",
            "Deployment & Service Orchestration",
            "Security Scanning & Compliance",
            "CKA/CKS Best Practices",
            "K8sGPT Integration",
            "Multi-Cluster Operations",
            "Performance Monitoring",
            "Troubleshooting & Debugging",
            "RBAC & Security Policies",
            "Network Policies & Security"
        ],
        "certifications": [
            "Certified Kubernetes Administrator (CKA)",
            "Certified Kubernetes Security Specialist (CKS)",
            "K8sGPT Integration Specialist"
        ],
        "focus_areas": [
            "Cluster Security Hardening",
            "Performance Optimization",
            "Automated Deployment Pipelines",
            "Multi-Environment Management",
            "Disaster Recovery",
            "Compliance & Governance"
        ]
    }

def _analyze_k8s_components(task_text: str) -> Dict[str, Any]:
    """Analyze task for Kubernetes components"""
    k8s_keywords = {
        "deployment": ["deploy", "deployment", "pod", "replicaset", "scale"],
        "service": ["service", "ingress", "loadbalancer", "clusterip"],
        "security": ["security", "rbac", "networkpolicy", "podsecurity", "seccomp"],
        "storage": ["pvc", "pv", "storageclass", "persistentvolume"],
        "monitoring": ["monitoring", "metrics", "logging", "prometheus", "grafana"],
        "networking": ["network", "ingress", "egress", "service mesh", "istio"]
    }
    
    components = {}
    task_lower = task_text.lower()
    
    for category, keywords in k8s_keywords.items():
        components[category] = any(keyword in task_lower for keyword in keywords)
    
    return components

def _generate_k8s_solution(task_text: str, k8s_components: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Kubernetes solution"""
    solution = {
        "approach": "kubernetes-native",
        "components": [],
        "security_level": "high",
        "scalability": "auto-scaling"
    }
    
    if k8s_components.get("deployment"):
        solution["components"].append("Deployment with Rolling Updates")
    
    if k8s_components.get("service"):
        solution["components"].append("Service with Load Balancing")
    
    if k8s_components.get("security"):
        solution["components"].append("Security Policies & RBAC")
    
    if k8s_components.get("storage"):
        solution["components"].append("Persistent Storage")
    
    return solution

def _generate_yaml_manifests(task_text: str, k8s_components: Dict[str, Any]) -> List[str]:
    """Generate YAML manifests"""
    manifests = []
    
    if k8s_components.get("deployment"):
        manifests.append("""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  labels:
    app: secure-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: app
        image: secure-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
        """)
    
    if k8s_components.get("security"):
        manifests.append("""
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-app-network-policy
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
        """)
    
    return manifests

def _generate_security_recommendations(task_text: str, k8s_components: Dict[str, Any]) -> List[str]:
    """Generate security recommendations"""
    recommendations = [
        "Enable Pod Security Standards (PSS)",
        "Implement Network Policies for pod-to-pod communication",
        "Use RBAC with least privilege principle",
        "Enable audit logging for security monitoring",
        "Regular security scanning with tools like Trivy"
    ]
    
    if k8s_components.get("security"):
        recommendations.extend([
            "Implement mTLS for service-to-service communication",
            "Use security contexts to run containers as non-root",
            "Enable seccomp profiles for additional security"
        ])
    
    return recommendations

def _generate_k8s_response(task_text: str, k8s_components: Dict[str, Any]) -> str:
    """Generate Kubernetes-focused response"""
    if k8s_components.get("deployment"):
        return "I'll help you create a secure Kubernetes deployment with proper resource limits and health checks."
    elif k8s_components.get("security"):
        return "I'll implement security best practices including RBAC, network policies, and pod security standards."
    elif k8s_components.get("service"):
        return "I'll set up proper service networking with load balancing and ingress configuration."
    else:
        return "I'm here to help with Kubernetes operations. What specific K8s challenge are you facing?"

def _calculate_confidence(k8s_components: Dict[str, Any]) -> float:
    """Calculate confidence score based on K8s components"""
    confidence = 0.6  # Base confidence for K8s specialist
    
    if k8s_components.get("deployment"):
        confidence += 0.15
    if k8s_components.get("security"):
        confidence += 0.2
    if k8s_components.get("service"):
        confidence += 0.1
    
    return min(confidence, 1.0)

def _simulate_k8sgpt_analysis(cluster_info: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate K8sGPT cluster analysis"""
    return {
        "insights": [
            "Cluster has 3 nodes with good resource distribution",
            "Security policies are properly configured",
            "Network policies need improvement"
        ],
        "recommendations": [
            "Implement stricter network policies",
            "Enable pod security standards",
            "Add resource quotas for namespaces"
        ],
        "security_issues": [
            "Some pods running as root",
            "Missing network policies in default namespace"
        ],
        "performance_optimizations": [
            "Consider horizontal pod autoscaling",
            "Optimize resource requests and limits"
        ]
    } 