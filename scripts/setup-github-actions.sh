#!/bin/bash

# Setup script for GitHub Actions AKS deployment
# This script helps configure the necessary Azure resources and GitHub secrets

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Configuration variables
SUBSCRIPTION_ID=""
RESOURCE_GROUP_DEMO="linkops-demo-rg"
RESOURCE_GROUP_PERSONAL="linkops-personal-rg"
CLUSTER_DEMO="linkops-demo-aks"
CLUSTER_PERSONAL="linkops-personal-aks"
SERVICE_PRINCIPAL_NAME="LinkOps-MLOps-GitHubActions"
GITHUB_REPO="your-org/LinkOps-MLOps"

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if user is logged in
    if ! az account show &> /dev/null; then
        print_error "Not logged into Azure. Please run 'az login' first."
        exit 1
    fi
    
    # Get current subscription
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    print_success "Using subscription: $SUBSCRIPTION_ID"
}

# Function to create service principal
create_service_principal() {
    print_status "Creating service principal..."
    
    # Create service principal
    SP_OUTPUT=$(az ad sp create-for-rbac \
        --name "$SERVICE_PRINCIPAL_NAME" \
        --role contributor \
        --scopes "/subscriptions/$SUBSCRIPTION_ID" \
        --sdk-auth)
    
    # Extract values
    CLIENT_ID=$(echo "$SP_OUTPUT" | jq -r '.clientId')
    CLIENT_SECRET=$(echo "$SP_OUTPUT" | jq -r '.clientSecret')
    TENANT_ID=$(echo "$SP_OUTPUT" | jq -r '.tenantId')
    
    print_success "Service principal created: $CLIENT_ID"
    
    # Store values for later use
    echo "CLIENT_ID=$CLIENT_ID" > .env.service-principal
    echo "CLIENT_SECRET=$CLIENT_SECRET" >> .env.service-principal
    echo "TENANT_ID=$TENANT_ID" >> .env.service-principal
    echo "SUBSCRIPTION_ID=$SUBSCRIPTION_ID" >> .env.service-principal
}

# Function to configure OIDC
configure_oidc() {
    print_status "Configuring OIDC for GitHub Actions..."
    
    # Get the application ID
    APP_ID=$(az ad app list --display-name "$SERVICE_PRINCIPAL_NAME" --query '[0].appId' -o tsv)
    
    # Create OIDC provider
    az ad app federated-credential create \
        --id "$APP_ID" \
        --parameters "{\"name\":\"github-actions\",\"issuer\":\"https://token.actions.githubusercontent.com\",\"subject\":\"repo:$GITHUB_REPO:ref:refs/heads/main\",\"audience\":\"api://AzureADTokenExchange\"}"
    
    print_success "OIDC configured for GitHub Actions"
}

# Function to assign AKS permissions
assign_aks_permissions() {
    print_status "Assigning AKS permissions..."
    
    # Assign permissions for demo cluster
    if az aks show --resource-group "$RESOURCE_GROUP_DEMO" --name "$CLUSTER_DEMO" &> /dev/null; then
        az role assignment create \
            --assignee "$CLIENT_ID" \
            --role "Azure Kubernetes Service Cluster User Role" \
            --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_DEMO/providers/Microsoft.ContainerService/managedClusters/$CLUSTER_DEMO"
        print_success "Permissions assigned for demo cluster"
    else
        print_warning "Demo cluster not found, skipping permissions"
    fi
    
    # Assign permissions for personal cluster
    if az aks show --resource-group "$RESOURCE_GROUP_PERSONAL" --name "$CLUSTER_PERSONAL" &> /dev/null; then
        az role assignment create \
            --assignee "$CLIENT_ID" \
            --role "Azure Kubernetes Service Cluster User Role" \
            --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_PERSONAL/providers/Microsoft.ContainerService/managedClusters/$CLUSTER_PERSONAL"
        print_success "Permissions assigned for personal cluster"
    else
        print_warning "Personal cluster not found, skipping permissions"
    fi
}

# Function to generate Helm charts
generate_helm_charts() {
    print_status "Generating Helm charts..."
    
    if [ -f "./scripts/generate-helm-charts.sh" ]; then
        ./scripts/generate-helm-charts.sh
        print_success "Helm charts generated"
    else
        print_warning "Helm chart generation script not found"
    fi
}

# Function to display next steps
display_next_steps() {
    print_success "Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Add the following secrets to your GitHub repository:"
    echo "   - AZURE_CLIENT_ID: $CLIENT_ID"
    echo "   - AZURE_TENANT_ID: $TENANT_ID"
    echo "   - AZURE_SUBSCRIPTION_ID: $SUBSCRIPTION_ID"
    echo
    echo "2. Optional secrets (if using these services):"
    echo "   - GITGUARDIAN_API_KEY: Your GitGuardian API key"
    echo "   - SONAR_TOKEN: Your SonarCloud token"
    echo "   - SONAR_ORG: Your SonarCloud organization"
    echo "   - SONAR_PROJECT_KEY: Your SonarCloud project key"
    echo
    echo "3. Update the GitHub repository name in the workflow file:"
    echo "   - Edit .github/workflows/deploy-aks.yml"
    echo "   - Replace 'your-org/LinkOps-MLOps' with your actual repository"
    echo
    echo "4. Test the deployment:"
    echo "   - Push changes to trigger the workflow"
    echo "   - Or manually trigger from GitHub Actions tab"
    echo
    echo "5. Review the documentation:"
    echo "   - docs/GITHUB_ACTIONS_SETUP.md"
    echo
    print_warning "The .env.service-principal file contains sensitive information. Keep it secure!"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up temporary files..."
    rm -f .env.service-principal
    print_success "Cleanup completed"
}

# Main execution
main() {
    echo "GitHub Actions AKS Deployment Setup"
    echo "=================================="
    echo
    
    # Check if user wants to proceed
    read -p "This script will create Azure resources and configure GitHub Actions. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setup cancelled"
        exit 0
    fi
    
    # Update GitHub repository name
    read -p "Enter your GitHub repository (format: org/repo): " GITHUB_REPO
    if [ -z "$GITHUB_REPO" ]; then
        print_error "GitHub repository is required"
        exit 1
    fi
    
    # Run setup steps
    check_prerequisites
    create_service_principal
    configure_oidc
    assign_aks_permissions
    generate_helm_charts
    display_next_steps
    
    # Ask if user wants to clean up
    read -p "Remove temporary files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
    fi
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --help, -h    Show this help message"
        echo "  --cleanup     Clean up temporary files"
        echo
        echo "This script sets up Azure resources and configuration for GitHub Actions AKS deployment."
        exit 0
        ;;
    --cleanup)
        cleanup
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac 