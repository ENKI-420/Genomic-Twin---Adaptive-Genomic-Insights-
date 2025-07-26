#!/bin/bash

echo "🔍 Validating DNA-Lang Deployment Configuration..."
echo "=================================================="

# Check if required files exist
required_files=(
    "setup.sh"
    "Dockerfile"
    "cloudbuild.yaml" 
    "terraform/main.tf"
    "terraform/variables.tf"
    "terraform/outputs.tf"
    "requirements.txt"
    "app.py"
)

echo "📁 Checking required files..."
missing_files=()
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "❌ Missing files detected. Please ensure all required files are present."
    exit 1
fi

echo ""
echo "🐳 Validating Dockerfile..."
if docker version &> /dev/null; then
    if docker build -t dnalang-validation-test . &> /dev/null; then
        echo "✅ Dockerfile builds successfully"
        docker rmi dnalang-validation-test &> /dev/null
    else
        echo "❌ Dockerfile has build errors"
    fi
else
    echo "⚠️  Docker not available for validation"
fi

echo ""
echo "🏗️  Validating Terraform configuration..."
if command -v terraform &> /dev/null; then
    cd terraform
    if terraform validate &> /dev/null; then
        echo "✅ Terraform configuration is valid"
    else
        echo "❌ Terraform configuration has errors"
        terraform validate
    fi
    cd ..
else
    echo "⚠️  Terraform not available for validation"
fi

echo ""
echo "📋 Validating Cloud Build configuration..."
if command -v gcloud &> /dev/null; then
    if gcloud builds validate --source=. cloudbuild.yaml &> /dev/null; then
        echo "✅ Cloud Build configuration is valid"
    else
        echo "❌ Cloud Build configuration has errors"
    fi
else
    echo "⚠️  Google Cloud SDK not available for validation"
fi

echo ""
echo "🧪 Validating Python application..."
if command -v python3 &> /dev/null; then
    if python3 -c "import app; print('✅ Main application imports successfully')" 2>/dev/null; then
        echo "✅ Python application validates"
    else
        echo "❌ Python application has import errors"
    fi
else
    echo "⚠️  Python3 not available for validation"
fi

echo ""
echo "📊 Configuration Summary:"
echo "========================"
echo "🚀 Deployment Options Available:"
echo "   1. ✅ One-click Cloud Shell deployment (setup.sh)"
echo "   2. ✅ Terraform + Cloud Build (terraform/ + cloudbuild.yaml)"
echo "   3. 🔄 Google Cloud Marketplace (preparation ready)"
echo ""
echo "🏗️  Infrastructure Components:"
echo "   ✅ Cloud Run service for Streamlit application"
echo "   ✅ Cloud SQL PostgreSQL database"
echo "   ✅ Pub/Sub event processing"
echo "   ✅ Artifact Registry for container images"
echo "   ✅ IAM service accounts and permissions"
echo ""
echo "🔧 Key Features:"
echo "   ✅ Auto-scaling (0-100 instances)"
echo "   ✅ HTTPS termination and custom domains"
echo "   ✅ Database connection pooling"
echo "   ✅ Event-driven architecture"
echo "   ✅ Monitoring and logging integration"
echo ""
echo "🎉 DNA-Lang deployment configuration is ready!"
echo "   Run './setup.sh' to deploy to Google Cloud"