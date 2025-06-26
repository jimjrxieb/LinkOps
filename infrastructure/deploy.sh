#!/bin/bash

# LinkOps Platform Engineering Stack Deployment Script
# This script deploys the complete LinkOps infrastructure on Azure

# =============================================================================
# 🔐 SECURITY: Environment Variable Validation
# =============================================================================
: "${GRAFANA_ADMIN_PASSWORD:?Environment variable GRAFANA_ADMIN_PASSWORD not set}"
: "${POSTGRES_PASSWORD:?Environment variable POSTGRES_PASSWORD not set}"

# =============================================================================
# 🎨 Color Functions for Output
# =============================================================================

set -e

echo "🚀 LinkOps Platform Engineering Stack Deployment"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    print_error "Terraform is not installed. Please install it first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install it first."
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed. Please install it first."
    exit 1
fi

print_status "All required tools are installed."

# Login to Azure
print_status "Logging in to Azure..."
az login

# Set subscription (optional - uncomment and modify if needed)
# print_status "Setting Azure subscription..."
# az account set --subscription "your-subscription-id"

# Navigate to Terraform directory
cd infrastructure/terraform

# Initialize Terraform
print_status "Initializing Terraform..."
terraform init

# Plan Terraform deployment
print_status "Planning Terraform deployment..."
terraform plan -out=tfplan

# Ask for confirmation
echo
read -p "Do you want to proceed with the deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Deployment cancelled."
    exit 0
fi

# Apply Terraform
print_status "Applying Terraform configuration..."
terraform apply tfplan

# Get outputs
print_status "Getting Terraform outputs..."
KUBECONFIG=$(terraform output -raw aks_kube_config)
ACR_LOGIN_SERVER=$(terraform output -raw acr_login_server)
ACR_USERNAME=$(terraform output -raw acr_admin_username)
ACR_PASSWORD=$(terraform output -raw acr_admin_password)

# Save kubeconfig
print_status "Saving kubeconfig..."
mkdir -p ~/.kube
echo "$KUBECONFIG" > ~/.kube/config
chmod 600 ~/.kube/config

# Wait for AKS to be ready
print_status "Waiting for AKS cluster to be ready..."
kubectl wait --for=condition=ready node --all --timeout=300s

# Add Helm repositories
print_status "Adding Helm repositories..."
helm repo add argo https://argoproj.github.io/argo-helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX Ingress Controller
print_status "Installing NGINX Ingress Controller..."
helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set controller.service.type=LoadBalancer

# Wait for ingress controller
print_status "Waiting for NGINX Ingress Controller..."
kubectl wait --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=300s

# Get ingress external IP
INGRESS_IP=$(kubectl get service nginx-ingress-ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
print_success "NGINX Ingress Controller external IP: $INGRESS_IP"

# Install ArgoCD
print_status "Installing ArgoCD..."
helm install argocd argo/argo-cd \
    --namespace argocd \
    --create-namespace \
    --set server.extraArgs[0]=--insecure \
    --set server.ingress.enabled=true \
    --set server.ingress.annotations."kubernetes\.io/ingress\.class"=nginx \
    --set server.ingress.hosts[0]=argocd.linkops.local

# Wait for ArgoCD
print_status "Waiting for ArgoCD to be ready..."
kubectl wait --namespace argocd \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/name=argocd-server \
    --timeout=300s

# Get ArgoCD admin password
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
print_success "ArgoCD admin password: $ARGOCD_PASSWORD"

# Install Prometheus Stack
print_status "Installing Prometheus Stack..."
helm install monitoring prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --set grafana.adminPassword=${GRAFANA_ADMIN_PASSWORD} \
    --set grafana.ingress.enabled=true \
    --set grafana.ingress.annotations."kubernetes\.io/ingress\.class"=nginx \
    --set grafana.ingress.hosts[0]=grafana.linkops.local

# Install Loki Stack
print_status "Installing Loki Stack..."
helm install loki grafana/loki-stack \
    --namespace logging \
    --create-namespace \
    --set loki.persistence.enabled=true \
    --set loki.persistence.storageClassName=managed-premium \
    --set loki.persistence.size=10Gi \
    --set grafana.enabled=false \
    --set promtail.enabled=true

# Create ArgoCD Application for LinkOps
print_status "Creating ArgoCD Application for LinkOps..."
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: linkops-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/$(git config user.name)/linkops.git
    targetRevision: main
    path: infrastructure/k8s/app
  destination:
    server: https://kubernetes.default.svc
    namespace: linkops
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
EOF

# Display deployment summary
echo
echo "🎉 LinkOps Platform Engineering Stack Deployment Complete!"
echo "========================================================"
echo
echo "📋 Deployment Summary:"
echo "  • AKS Cluster: $(terraform output -raw aks_cluster_name)"
echo "  • Resource Group: $(terraform output -raw resource_group_name)"
echo "  • Container Registry: $ACR_LOGIN_SERVER"
echo "  • Ingress External IP: $INGRESS_IP"
echo
echo "🔗 Access URLs:"
echo "  • ArgoCD: http://argocd.linkops.local (admin / $ARGOCD_PASSWORD)"
echo "  • Grafana: http://grafana.linkops.local (admin / ${GRAFANA_ADMIN_PASSWORD})"
echo "  • LinkOps Frontend: http://linkops.local"
echo "  • LinkOps API: http://api.linkops.local"
echo
echo "📝 Next Steps:"
echo "  1. Add DNS records pointing to $INGRESS_IP:"
echo "     - argocd.linkops.local"
echo "     - grafana.linkops.local"
echo "     - linkops.local"
echo "     - api.linkops.local"
echo "  2. Set up GitHub Actions secrets:"
echo "     - ACR_LOGIN_SERVER: $ACR_LOGIN_SERVER"
echo "     - ACR_USERNAME: $ACR_USERNAME"
echo "     - ACR_PASSWORD: $ACR_PASSWORD"
echo "     - KUBECONFIG: <base64-encoded-kubeconfig>"
echo "  3. Push your code to trigger the CI/CD pipeline"
echo
echo "🔧 Useful Commands:"
echo "  • View ArgoCD applications: kubectl get applications -n argocd"
echo "  • View LinkOps pods: kubectl get pods -n linkops"
echo "  • View monitoring pods: kubectl get pods -n monitoring"
echo "  • Port forward ArgoCD: kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo
print_success "Deployment completed successfully!" 