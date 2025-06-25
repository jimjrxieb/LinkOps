#!/bin/bash

# =============================================================================
# GitHub Secrets Setup Script for LinkOps Core
# =============================================================================
# This script helps you set up GitHub Secrets for AKS deployment
# Run this script after setting up your Azure resources

set -e

echo "🔐 LinkOps Core - GitHub Secrets Setup"
echo "======================================"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed. Please install it first:"
    echo "   https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub. Please run: gh auth login"
    exit 1
fi

echo "📋 Setting up GitHub Secrets..."
echo ""

# Function to prompt for secret value
prompt_secret() {
    local secret_name=$1
    local description=$2
    local is_required=${3:-true}
    
    echo "🔑 $description"
    if [ "$is_required" = "true" ]; then
        echo "   (Required)"
    else
        echo "   (Optional)"
    fi
    
    read -s -p "   Enter value: " secret_value
    echo ""
    
    if [ -n "$secret_value" ]; then
        echo "   Setting $secret_name..."
        echo "$secret_value" | gh secret set "$secret_name"
        echo "   ✅ $secret_name set successfully"
    elif [ "$is_required" = "true" ]; then
        echo "   ❌ $secret_name is required!"
        exit 1
    else
        echo "   ⏭️  Skipping $secret_name (optional)"
    fi
    echo ""
}

# Required Azure Secrets
echo "🌐 AZURE CONFIGURATION"
echo "======================"

prompt_secret "AZURE_CREDENTIALS" "Azure Service Principal credentials (JSON)"
prompt_secret "AZURE_SUBSCRIPTION_ID" "Azure Subscription ID"
prompt_secret "AZURE_RESOURCE_GROUP" "Azure Resource Group name"
prompt_secret "AZURE_AKS_CLUSTER_NAME" "Azure Kubernetes Service cluster name"
prompt_secret "AZURE_AKS_RESOURCE_GROUP" "AKS Resource Group name"
prompt_secret "AZURE_ACR_NAME" "Azure Container Registry name"
prompt_secret "AZURE_ACR_USERNAME" "Azure Container Registry username"
prompt_secret "AZURE_ACR_PASSWORD" "Azure Container Registry password"

# Required Application Secrets
echo "🔧 APPLICATION SECRETS"
echo "======================"

prompt_secret "OPENAI_API_KEY" "OpenAI API Key (starts with sk-)"
prompt_secret "POSTGRES_PASSWORD" "PostgreSQL database password"
prompt_secret "SECRET_KEY" "Application secret key (generate with: openssl rand -hex 32)"

# Optional Secrets
echo "📊 OPTIONAL SECRETS"
echo "=================="

prompt_secret "AZURE_APPINSIGHTS_CONNECTION_STRING" "Azure Application Insights connection string" "false"
prompt_secret "TEST_DATABASE_URL" "Test database URL for CI/CD" "false"

# Azure Key Vault (optional)
echo "🗄️ AZURE KEY VAULT (OPTIONAL)"
echo "============================="

prompt_secret "AZURE_KEY_VAULT_NAME" "Azure Key Vault name for production secrets" "false"
prompt_secret "AZURE_CLIENT_ID" "Azure Workload Identity client ID" "false"

echo "✅ GitHub Secrets setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Push your code to trigger the GitHub Actions workflow"
echo "2. Monitor the deployment in the Actions tab"
echo "3. Check your AKS cluster for the deployed services"
echo ""
echo "🔍 To verify secrets are set:"
echo "   gh secret list"
echo ""
echo "🗑️  To remove a secret:"
echo "   gh secret delete SECRET_NAME" 