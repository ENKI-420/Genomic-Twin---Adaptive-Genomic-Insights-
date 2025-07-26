#!/bin/bash
set -e

echo "🚀 Starting DNA-Lang Genomic Twin Deployment..."
echo "======================================================"

# Check if fzf is available, if not provide fallback
if command -v fzf &> /dev/null; then
    echo "📋 Please select a Google Cloud Project:"
    PROJECT_ID=$(gcloud projects list --format='value(PROJECT_ID)' | fzf --prompt "Select a Google Cloud Project: ")
else
    echo "📋 Available Google Cloud Projects:"
    gcloud projects list --format="table(PROJECT_ID,NAME)"
    echo ""
    read -p "Please enter your Google Cloud Project ID: " PROJECT_ID
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project selected. Exiting..."
    exit 1
fi

gcloud config set project $PROJECT_ID
echo "✅ Project set to: $PROJECT_ID"

# Enable required APIs
echo "⚙️  Enabling necessary APIs..."
gcloud services enable \
    run.googleapis.com \
    iam.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    cloudsql.googleapis.com \
    pubsub.googleapis.com \
    --quiet

echo "✅ APIs enabled successfully"

# Set default region
REGION="us-central1"
gcloud config set run/region $REGION

# Create Artifact Registry repository for container images
echo "🏗️  Creating Artifact Registry repository..."
gcloud artifacts repositories create dnalang-repo \
    --repository-format=docker \
    --location=$REGION \
    --description="DNA-Lang Genomic Twin container repository" \
    --quiet || echo "Repository may already exist"

# Create Cloud SQL instance for genomic data storage
echo "🗄️  Provisioning Cloud SQL for PostgreSQL..."
gcloud sql instances create dnalang-genomic-db \
    --database-version=POSTGRES_14 \
    --region=$REGION \
    --cpu=1 \
    --memory=4GiB \
    --storage-size=20GB \
    --storage-type=SSD \
    --availability-type=zonal \
    --quiet || echo "Database instance may already exist"

# Create database and user
echo "👤 Setting up database and user..."
gcloud sql databases create genomic_twin_db --instance=dnalang-genomic-db --quiet || echo "Database may already exist"
gcloud sql users create dnauser --instance=dnalang-genomic-db --password=genomic_twin_2024 --quiet || echo "User may already exist"

# Create Pub/Sub topic for event processing
echo "📡 Setting up Pub/Sub event bus..."
gcloud pubsub topics create dnalang-genomic-events --quiet || echo "Topic may already exist"
gcloud pubsub subscriptions create dnalang-genomic-events-sub --topic=dnalang-genomic-events --quiet || echo "Subscription may already exist"

# Build and deploy the main application to Cloud Run
echo "🐳 Building and deploying the Genomic Twin application to Cloud Run..."

# Create Dockerfile if it doesn't exist
if [ ! -f "Dockerfile" ]; then
    echo "📄 Creating Dockerfile..."
    cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
EOF
fi

# Build and submit container image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/dnalang-repo/genomic-twin-app:latest

# Deploy to Cloud Run with database connection
DB_CONNECTION_NAME="$PROJECT_ID:$REGION:dnalang-genomic-db"

gcloud run deploy dnalang-genomic-twin \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/dnalang-repo/genomic-twin-app:latest \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated \
    --memory=2Gi \
    --cpu=2 \
    --add-cloudsql-instances=$DB_CONNECTION_NAME \
    --set-env-vars="DATABASE_URL=postgresql://dnauser:genomic_twin_2024@/genomic_twin_db?host=/cloudsql/$DB_CONNECTION_NAME" \
    --set-env-vars="PROJECT_ID=$PROJECT_ID" \
    --set-env-vars="PUBSUB_TOPIC=dnalang-genomic-events" \
    --quiet

echo ""
echo "🎉 DNA-Lang Genomic Twin has been deployed successfully!"
echo "======================================================"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe dnalang-genomic-twin --platform=managed --region=$REGION --format='value(status.url)')

echo "🌐 Application URL: $SERVICE_URL"
echo "📊 Cloud Console: https://console.cloud.google.com/run/detail/$REGION/dnalang-genomic-twin/metrics?project=$PROJECT_ID"
echo "🗄️  Database: https://console.cloud.google.com/sql/instances/dnalang-genomic-db/overview?project=$PROJECT_ID"
echo "📡 Pub/Sub: https://console.cloud.google.com/cloudpubsub/topic/detail/dnalang-genomic-events?project=$PROJECT_ID"
echo ""
echo "✨ Your DNA-Lang Genomic Twin platform is now live and ready for genomic analysis!"
echo "🔬 Upload genomic data files (VCF/CSV) and start analyzing mutations and generating insights."