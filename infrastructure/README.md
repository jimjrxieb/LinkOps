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

```
infrastructure/
├── terraform/                 # Terraform configuration
│   ├── main.tf               # Main infrastructure
│   ├── variables.tf          # Variable definitions
│   ├── outputs.tf            # Output values
│   └── monitoring-setup.sh   # Monitoring VM setup script
├── k8s/                      # Kubernetes manifests
│   ├── argocd/              # ArgoCD installation
│   └── app/                 # LinkOps application manifests
├── deploy.sh                 # Automated deployment script
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Azure CLI** - [Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. **Terraform** - [Install Guide](https://www.terraform.io/downloads.html)
3. **kubectl** - [Install Guide](https://kubernetes.io/docs/tasks/tools/)
4. **Helm** - [Install Guide](https://helm.sh/docs/intro/install/)

### Automated Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/linkops.git
cd linkops

# Run the deployment script
chmod +x infrastructure/deploy.sh
./infrastructure/deploy.sh
```

### Manual Deployment

```bash
# 1. Login to Azure
az login

# 2. Navigate to Terraform directory
cd infrastructure/terraform

# 3. Initialize Terraform
terraform init

# 4. Plan deployment
terraform plan -out=tfplan

# 5. Apply configuration
terraform apply tfplan

# 6. Get kubeconfig
terraform output -raw aks_kube_config > ~/.kube/config

# 7. Install ArgoCD
helm install argocd argo/argo-cd \
    --namespace argocd \
    --create-namespace \
    --set server.extraArgs[0]=--insecure

# 8. Install monitoring stack
helm install monitoring prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace
```

## 🏛️ Infrastructure Components

### 1. Azure Kubernetes Service (AKS)
- **Cluster Name**: `aks-linkops`
- **Node Count**: 2 (auto-scaling 1-5)
- **VM Size**: Standard_DS2_v2
- **Region**: East US
- **Network Plugin**: Azure CNI
- **Network Policy**: Azure

### 2. Azure Container Registry (ACR)
- **Name**: `linkopsacr`
- **SKU**: Basic
- **Admin Enabled**: Yes

### 3. ArgoCD (GitOps)
- **Namespace**: `argocd`
- **Access**: http://argocd.linkops.local
- **Admin Password**: Generated during deployment

### 4. Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visualization (http://grafana.linkops.local)
- **Loki**: Log aggregation
- **Namespace**: `monitoring`

### 5. LinkOps Applications
- **Backend**: FastAPI application
- **Frontend**: Vue.js application
- **PostgreSQL**: Database
- **Namespace**: `linkops`

## 🔧 Configuration

### Environment Variables

Create a `terraform.tfvars` file to customize the deployment:

```hcl
resource_group_name = "rg-linkops-demo"
location            = "East US"
cluster_name        = "aks-linkops"
node_count          = 2
vm_size             = "Standard_DS2_v2"
environment         = "demo"
project             = "linkops"
```

### GitHub Actions Secrets

Set these secrets in your GitHub repository:

- `ACR_LOGIN_SERVER`: Azure Container Registry login server
- `ACR_USERNAME`: ACR admin username
- `ACR_PASSWORD`: ACR admin password
- `KUBECONFIG`: Base64-encoded kubeconfig

## 📊 Monitoring & Observability

### Grafana Dashboards
- **Kubernetes Cluster Overview**
- **LinkOps Application Metrics**
- **Prometheus Targets**
- **Loki Logs**

### Prometheus Targets
- Kubernetes API servers
- Node metrics
- Pod metrics
- Custom LinkOps metrics

### Log Aggregation
- **Loki**: Centralized log storage
- **Promtail**: Log collection agent
- **Grafana**: Log visualization

## 🔐 Security

### Network Security
- Azure Network Security Groups
- Kubernetes Network Policies
- Ingress TLS termination

### Secrets Management
- Kubernetes Secrets
- Azure Key Vault integration (optional)
- HashiCorp Vault (optional)

## 🚨 Troubleshooting

### Common Issues

1. **AKS Cluster Not Ready**
   ```bash
   kubectl get nodes
   kubectl describe node <node-name>
   ```

2. **ArgoCD Not Accessible**
   ```bash
   kubectl get pods -n argocd
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

3. **Monitoring Stack Issues**
   ```bash
   kubectl get pods -n monitoring
   kubectl logs -n monitoring deployment/prometheus-operator
   ```

4. **Application Deployment Issues**
   ```bash
   kubectl get pods -n linkops
   kubectl describe pod <pod-name> -n linkops
   ```

### Useful Commands

```bash
# Get cluster info
kubectl cluster-info

# View all namespaces
kubectl get namespaces

# View ArgoCD applications
kubectl get applications -n argocd

# View LinkOps pods
kubectl get pods -n linkops

# View monitoring pods
kubectl get pods -n monitoring

# Port forward services
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

## 📈 Scaling

### Horizontal Pod Autoscaling
```bash
kubectl autoscale deployment linkops-backend -n linkops --cpu-percent=70 --min=2 --max=10
kubectl autoscale deployment linkops-frontend -n linkops --cpu-percent=70 --min=2 --max=10
```

### Cluster Autoscaling
The AKS cluster is configured with auto-scaling enabled (1-5 nodes).

## 🧹 Cleanup

To destroy the infrastructure:

```bash
cd infrastructure/terraform
terraform destroy
```

**Warning**: This will delete all resources including the AKS cluster and all data.

## 📚 Additional Resources

- [Azure AKS Documentation](https://docs.microsoft.com/en-us/azure/aks/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs) 