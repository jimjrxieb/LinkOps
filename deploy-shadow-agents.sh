#!/bin/bash

# 🛡️ Shadow Agents Deployment Script
# Deploys all LinkOps shadow agents using Helm and ArgoCD

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="linkops"
ARGOCD_NAMESPACE="argocd"
HELM_REPO="https://github.com/shadow-link-industries/LinkOps-Helm.git"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists kubectl; then
        print_error "kubectl is not installed"
        exit 1
    fi
    
    if ! command_exists helm; then
        print_error "helm is not installed"
        exit 1
    fi
    
    # Check cluster access
    if ! kubectl cluster-info >/dev/null 2>&1; then
        print_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to create namespace
create_namespace() {
    print_status "Creating namespace: $NAMESPACE"
    
    if ! kubectl get namespace $NAMESPACE >/dev/null 2>&1; then
        kubectl create namespace $NAMESPACE
        print_success "Namespace $NAMESPACE created"
    else
        print_warning "Namespace $NAMESPACE already exists"
    fi
}

# Function to create required secrets
create_secrets() {
    print_status "Creating required secrets..."
    
    # Check if OpenAI secret exists
    if ! kubectl get secret openai-secret -n $NAMESPACE >/dev/null 2>&1; then
        print_warning "OpenAI secret not found. Please create it manually:"
        echo "kubectl create secret generic openai-secret \\"
        echo "  --from-literal=key=your-openai-api-key \\"
        echo "  -n $NAMESPACE"
    else
        print_success "OpenAI secret exists"
    fi
    
    # Check if Katie kubeconfig secret exists
    if ! kubectl get secret katie-kubeconfig -n $NAMESPACE >/dev/null 2>&1; then
        print_warning "Katie kubeconfig secret not found. Please create it manually:"
        echo "kubectl create secret generic katie-kubeconfig \\"
        echo "  --from-file=config=\$HOME/.kube/config \\"
        echo "  -n $NAMESPACE"
    else
        print_success "Katie kubeconfig secret exists"
    fi
}

# Function to add Helm repository
add_helm_repo() {
    print_status "Adding Helm repository..."
    
    helm repo add linkops $HELM_REPO
    helm repo update
    print_success "Helm repository added and updated"
}

# Function to deploy agent
deploy_agent() {
    local agent_name=$1
    local chart_name=$2
    local image_repo=$3
    
    print_status "Deploying $agent_name..."
    
    if kubectl get deployment $agent_name-logic -n $NAMESPACE >/dev/null 2>&1; then
        print_warning "$agent_name is already deployed. Upgrading..."
        helm upgrade $agent_name-logic linkops/$chart_name \
            --namespace $NAMESPACE \
            --set image.repository=$image_repo \
            --set image.tag=latest \
            --wait
    else
        helm install $agent_name-logic linkops/$chart_name \
            --namespace $NAMESPACE \
            --set image.repository=$image_repo \
            --set image.tag=latest \
            --wait
    fi
    
    print_success "$agent_name deployed successfully"
}

# Function to deploy all agents
deploy_all_agents() {
    print_status "Deploying all shadow agents..."
    
    # Deploy Igris Logic
    deploy_agent "igris" "igris_logic" "ghcr.io/shadow-link-industries/igris_logic"
    
    # Deploy Katie Logic
    deploy_agent "katie" "katie_logic" "ghcr.io/shadow-link-industries/katie_logic"
    
    # Deploy Whis Logic
    deploy_agent "whis" "whis_logic" "ghcr.io/shadow-link-industries/whis_logic"
    
    # Deploy James Logic
    deploy_agent "james" "james_logic" "ghcr.io/shadow-link-industries/james_logic"
    
    print_success "All shadow agents deployed successfully"
}

# Function to check deployment status
check_deployment_status() {
    print_status "Checking deployment status..."
    
    echo ""
    echo "Deployment Status:"
    echo "=================="
    
    kubectl get deployments -n $NAMESPACE -o wide
    
    echo ""
    echo "Pod Status:"
    echo "==========="
    
    kubectl get pods -n $NAMESPACE -o wide
    
    echo ""
    echo "Service Status:"
    echo "==============="
    
    kubectl get services -n $NAMESPACE
}

# Function to show access information
show_access_info() {
    print_status "Shadow Agents Access Information"
    echo ""
    echo "Services:"
    echo "========="
    echo "Igris Logic:   http://igris-logic:8000"
    echo "Katie Logic:   http://katie-logic:8000"
    echo "Whis Logic:    http://whis-logic:8000"
    echo "James Logic:   http://james-logic:8000"
    echo ""
    echo "Health Endpoints:"
    echo "================="
    echo "Igris Logic:   http://igris-logic:8000/health"
    echo "Katie Logic:   http://katie-logic:8000/health"
    echo "Whis Logic:    http://whis-logic:8000/health"
    echo "James Logic:   http://james-logic:8000/health"
    echo ""
    echo "To access services from outside the cluster:"
    echo "============================================"
    echo "kubectl port-forward svc/igris-logic 8001:8000 -n $NAMESPACE"
    echo "kubectl port-forward svc/katie-logic 8002:8000 -n $NAMESPACE"
    echo "kubectl port-forward svc/whis-logic 8003:8000 -n $NAMESPACE"
    echo "kubectl port-forward svc/james-logic 8004:8000 -n $NAMESPACE"
}

# Function to deploy using ArgoCD
deploy_with_argocd() {
    print_status "Deploying using ArgoCD..."
    
    # Check if ArgoCD is installed
    if ! kubectl get namespace $ARGOCD_NAMESPACE >/dev/null 2>&1; then
        print_error "ArgoCD namespace not found. Please install ArgoCD first."
        exit 1
    fi
    
    # Apply ArgoCD applications
    if [ -d "LinkOps-Manifests/services" ]; then
        kubectl apply -f LinkOps-Manifests/shadows/
        print_success "ArgoCD applications applied"
    else
        print_error "LinkOps-Manifests/services directory not found"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "🛡️ Shadow Agents Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --helm          Deploy using Helm (default)"
    echo "  --argocd        Deploy using ArgoCD"
    echo "  --status        Check deployment status"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              Deploy all agents using Helm"
    echo "  $0 --argocd     Deploy all agents using ArgoCD"
    echo "  $0 --status     Check deployment status"
}

# Main script
main() {
    echo "🛡️ Shadow Agents Deployment Script"
    echo "=================================="
    echo ""
    
    # Parse command line arguments
    case "${1:-}" in
        --helm)
            DEPLOY_METHOD="helm"
            ;;
        --argocd)
            DEPLOY_METHOD="argocd"
            ;;
        --status)
            check_prerequisites
            check_deployment_status
            exit 0
            ;;
        --help)
            show_help
            exit 0
            ;;
        "")
            DEPLOY_METHOD="helm"
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    
    # Execute deployment
    check_prerequisites
    create_namespace
    create_secrets
    
    if [ "$DEPLOY_METHOD" = "argocd" ]; then
        deploy_with_argocd
    else
        add_helm_repo
        deploy_all_agents
    fi
    
    check_deployment_status
    show_access_info
    
    print_success "Shadow agents deployment completed!"
    echo ""
    echo "Next steps:"
    echo "1. Verify all pods are running: kubectl get pods -n $NAMESPACE"
    echo "2. Check agent health: curl http://igris-logic:8000/health"
    echo "3. Access ArgoCD UI (if using ArgoCD): kubectl port-forward svc/argocd-server -n argocd 8080:443"
    echo "4. Review documentation: docs/deployment/shadow-agents.md"
}

# Run main function
main "$@" 