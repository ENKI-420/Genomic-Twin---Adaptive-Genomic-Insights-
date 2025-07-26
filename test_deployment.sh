#!/bin/bash

echo "🧪 DNA-Lang Deployment Testing Script"
echo "====================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Test 1: Check Docker build locally
echo "📦 Testing Docker container build..."
if command_exists docker; then
    # Try a quick syntax check first
    if docker build --help >/dev/null 2>&1; then
        echo "✅ Docker is available and working"
        echo "   Note: Full build test available via: docker build -t dnalang-test ."
    else
        echo "❌ Docker is not functioning properly"
    fi
else
    echo "⚠️  Docker not available - skipping container test"
fi

# Test 2: Validate Terraform configuration
echo ""
echo "🏗️  Testing Terraform configuration..."
if command_exists terraform; then
    cd terraform
    if terraform validate >/dev/null 2>&1; then
        echo "✅ Terraform configuration is valid"
    else
        echo "❌ Terraform validation failed"
        echo "   Run: cd terraform && terraform validate"
    fi
    cd ..
else
    echo "⚠️  Terraform not available - skipping validation"
fi

# Test 3: Check Google Cloud authentication
echo ""
echo "🔐 Testing Google Cloud authentication..."
if command_exists gcloud; then
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" >/dev/null 2>&1; then
        ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
        echo "✅ Authenticated as: $ACTIVE_ACCOUNT"
        
        # Check current project
        CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
        if [ -n "$CURRENT_PROJECT" ]; then
            echo "✅ Current project: $CURRENT_PROJECT"
        else
            echo "⚠️  No default project set"
            echo "   Run: gcloud config set project YOUR_PROJECT_ID"
        fi
    else
        echo "❌ Not authenticated with Google Cloud"
        echo "   Run: gcloud auth login"
    fi
else
    echo "⚠️  Google Cloud SDK not available"
fi

# Test 4: Check Python dependencies
echo ""
echo "🐍 Testing Python application..."
if command_exists python3; then
    # Create a temporary virtual environment for testing
    if python3 -m venv test_env >/dev/null 2>&1; then
        source test_env/bin/activate
        
        if pip install -r requirements.txt >/dev/null 2>&1; then
            if python3 -c "import streamlit; print('✅ Streamlit imported successfully')" 2>/dev/null; then
                echo "✅ Python dependencies install correctly"
            else
                echo "❌ Python import test failed"
            fi
        else
            echo "❌ Failed to install Python dependencies"
        fi
        
        deactivate
        rm -rf test_env
    else
        echo "❌ Failed to create test environment"
    fi
else
    echo "⚠️  Python3 not available - skipping dependency test"
fi

# Test 5: Test setup script syntax
echo ""
echo "📜 Testing setup script..."
if bash -n setup.sh >/dev/null 2>&1; then
    echo "✅ Setup script syntax is valid"
else
    echo "❌ Setup script has syntax errors"
    echo "   Run: bash -n setup.sh"
fi

# Test 6: Test Cloud Build configuration
echo ""
echo "☁️  Testing Cloud Build configuration..."
if command_exists gcloud; then
    # Check if cloudbuild.yaml syntax is valid YAML
    if command_exists python3; then
        python3 -c "import yaml; yaml.safe_load(open('cloudbuild.yaml'))" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Cloud Build configuration YAML is valid"
        else
            echo "❌ Cloud Build configuration has YAML syntax errors"
        fi
    else
        echo "⚠️  Cannot validate YAML syntax - Python3 not available"
    fi
else
    echo "⚠️  Google Cloud SDK not available - skipping Cloud Build test"
fi

echo ""
echo "📋 Test Summary"
echo "==============="
echo "🚀 Ready to deploy? Choose your deployment method:"
echo ""
echo "1. 🎯 Quick Start (Recommended for first-time users):"
echo "   ./setup.sh"
echo ""
echo "2. 🏗️  Production Deployment:"
echo "   gcloud builds submit --config=cloudbuild.yaml"
echo ""
echo "3. 🔧 Manual Terraform:"
echo "   cd terraform && terraform init && terraform plan"
echo ""
echo "📚 For detailed instructions, see: DEPLOYMENT_GUIDE.md"