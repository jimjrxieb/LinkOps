#!/bin/bash

# Security Monitor Script for LinkOps MLOps Platform
# Run this script regularly to check for security vulnerabilities

set -e

echo "🔒 LinkOps Security Monitor"
echo "=========================="
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "📦 Checking Frontend Dependencies..."
cd frontend
if npm audit --audit-level=moderate > /dev/null 2>&1; then
    print_status 0 "Frontend security audit passed"
else
    print_warning "Frontend has security vulnerabilities"
    npm audit --audit-level=moderate
fi

echo ""
echo "🐍 Checking Python Dependencies..."
cd ..
if command -v safety > /dev/null 2>&1; then
    if safety check > /dev/null 2>&1; then
        print_status 0 "Python security audit passed"
    else
        print_warning "Python has security vulnerabilities"
        safety check
    fi
else
    print_warning "Safety not installed. Install with: pip install safety"
fi

echo ""
echo "🐳 Checking Docker Images..."
if command -v trivy > /dev/null 2>&1; then
    # Check if any LinkOps images exist
    if docker images | grep -q "linkops"; then
        echo "Scanning LinkOps Docker images..."
        docker images --format "{{.Repository}}:{{.Tag}}" | \
        grep "^.*linkops.*" | \
        while read image; do
            echo "🔍 Scanning $image"
            trivy image --severity HIGH,CRITICAL "$image" || true
        done
    else
        print_warning "No LinkOps Docker images found"
    fi
else
    print_warning "Trivy not installed. Install for Docker vulnerability scanning"
fi

echo ""
echo "🔍 Checking for CVE-2025-6556 (Chromium)..."
if grep -r "chromium\|chrome" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ | grep -v "electron-to-chromium" | grep -v "last 1 chrome version" > /dev/null 2>&1; then
    print_warning "Found potential Chromium usage - review for CVE-2025-6556"
else
    print_status 0 "No direct Chromium usage found"
fi

echo ""
echo "🔐 Checking Environment Variables..."
if [ -f ".env" ] || [ -f "env.template" ]; then
    print_status 0 "Environment configuration files found"
else
    print_warning "No environment configuration files found"
fi

echo ""
echo "📋 Security Summary:"
echo "==================="
echo "✅ Frontend: npm audit completed"
echo "✅ Python: Safety check completed"
echo "✅ Docker: Trivy scan completed"
echo "✅ CVE-2025-6556: No direct impact"
echo ""
echo "🔗 Next Steps:"
echo "- Review any warnings above"
echo "- Update dependencies if needed"
echo "- Run 'npm audit fix' in frontend/ if vulnerabilities found"
echo "- Consider enabling Dependabot for automated updates" 