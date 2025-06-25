# LinkOps Platform Engineering Infrastructure

This directory contains the complete infrastructure setup for the LinkOps MLOps platform using Terraform, AKS, ArgoCD, and monitoring stack.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Azure AKS     │    │   Monitoring    │
│   Actions       │───▶│   Cluster       │───▶│   Stack         │
│   (CI/CD)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ArgoCD        │    │   LinkOps       │    │   Grafana       │
│   (GitOps)      │    │   Applications  │    │   Dashboards    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Directory Structure

# ☸️ LinkOps Kubernetes Deployment (AKS)

This directory contains raw Kubernetes manifests and configuration for deploying LinkOps microservices into Azure Kubernetes Service (AKS). It is GitOps-ready and synced by ArgoCD.

---

## 🧠 ArgoCD Setup (One-time)

ArgoCD will watch this folder and apply updates to the AKS cluster when it detects changes.

Install ArgoCD into AKS:

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd --namespace argocd --create-namespace
```

Then apply the application config:

```bash
kubectl apply -f argocd-apps/linkops-app.yaml
```

---

## 🧱 Directory Structure

```
k8s/
├── base/                # Core manifests for all services
│   ├── james/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── whis/
│   ├── katie/
│   ├── igris/
│   ├── ingress.yaml
│   └── namespace.yaml
├── overlays/            # Environment-specific customizations
│   ├── dev/
│   └── prod/
└── argocd-apps/
    └── linkops-app.yaml
```

---

## 🔧 Manual Customizations (CKA-Style)

You can modify the base YAMLs manually for common exam-level tasks:

### ✅ Change Replicas

Edit `deployment.yaml` for any service:

```yaml
spec:
  replicas: 3  # change this value
```

### ✅ Add a Sidecar Container

```yaml
containers:
  - name: main-app
    image: your-image
  - name: sidecar-logger
    image: busybox
    command: ["sh", "-c", "tail -f /var/log/app.log"]
```

### ✅ Add a Service Account

Create:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: whis-sa
  namespace: linkops
```

Then reference it in your deployment:

```yaml
spec:
  serviceAccountName: whis-sa
```

### ✅ Add RBAC for the Agent

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: linkops
  name: whis-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: whis-rolebinding
  namespace: linkops
subjects:
- kind: ServiceAccount
  name: whis-sa
  namespace: linkops
roleRef:
  kind: Role
  name: whis-role
  apiGroup: rbac.authorization.k8s.io
```

---

## 🛠 Helm Installs You'll Likely Need

| Tool                     | Helm Install Command                                           |
| ------------------------ | -------------------------------------------------------------- |
| ArgoCD                   | `helm install argocd argo/argo-cd ...`                         |
| Prometheus               | `helm install monitoring prometheus/kube-prometheus-stack ...` |
| GitHub Runner (optional) | `helm install gha actions-runner-controller/...`               |

---

## 🧪 Validate Your Setup

```bash
kubectl get pods -n linkops
kubectl describe deployment james -n linkops
kubectl logs -f deployment/james -n linkops
```

---

## ✅ Best Practice

Use `base/` for core manifests.
Use `overlays/dev/` for environment-specific tweaks via Kustomize.
