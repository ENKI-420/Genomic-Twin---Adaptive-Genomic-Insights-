#!/bin/bash
set -e

echo "🚀 Starting DNA-Lang Autonomous Bio-Digital Platform Deployment..."
echo "=================================================================="

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
    compute.googleapis.com \
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
    --description="DNA-Lang Autonomous Bio-Digital Platform container repository" \
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
echo "🐳 Building and deploying the DNA-Lang Platform to Cloud Run..."

# Create optimized Dockerfile for the unified platform
echo "📄 Creating unified platform Dockerfile..."
cat > Dockerfile << 'EOF'
# DNA-Lang Autonomous Bio-Digital Platform Dockerfile
FROM node:18-slim AS backend-builder

WORKDIR /app/backend
COPY backend/ .
COPY package*.json ./
RUN npm install

FROM python:3.10-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final unified image
FROM python:3.10-slim

# Install Node.js for backend services
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend
COPY --from=backend-builder /app/backend ./backend
COPY --from=backend-builder /app/backend/node_modules ./backend/node_modules

# Copy frontend
COPY --from=frontend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY frontend/ ./frontend/

# Copy other files
COPY terraform/ ./terraform/
COPY setup.sh cloudbuild.yaml .env.example ./

# Install frontend dependencies
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Expose ports
EXPOSE 8080 8081

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app
ENV NODE_PATH=/app/backend

# Create startup script for unified platform
RUN echo '#!/bin/bash\n\
# Start backend services in background\n\
cd /app && node backend/evolution_engine.js &\n\
cd /app && node backend/agents/cloud_architect_agent.js &\n\
cd /app && node backend/agents/biography_agent.js &\n\
cd /app && node backend/agents/meta_cognition_agent.js &\n\
\n\
# Start frontend dashboard\n\
cd /app/frontend && streamlit run app.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
EOF

# Build and submit container image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/dnalang-repo/dna-lang-platform:latest

# Deploy to Cloud Run with database connection
DB_CONNECTION_NAME="$PROJECT_ID:$REGION:dnalang-genomic-db"

gcloud run deploy dna-lang-platform \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/dnalang-repo/dna-lang-platform:latest \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated \
    --memory=4Gi \
    --cpu=2 \
    --timeout=3600 \
    --concurrency=10 \
    --add-cloudsql-instances=$DB_CONNECTION_NAME \
    --set-env-vars="DATABASE_URL=postgresql://dnauser:genomic_twin_2024@/genomic_twin_db?host=/cloudsql/$DB_CONNECTION_NAME" \
    --set-env-vars="PROJECT_ID=$PROJECT_ID" \
    --set-env-vars="REGION=$REGION" \
    --set-env-vars="PUBSUB_TOPIC=dnalang-genomic-events" \
    --set-env-vars="EVOLUTION_TARGET_FITNESS=0.95" \
    --set-env-vars="EVOLUTION_TARGET_CONSCIOUSNESS=0.95" \
    --set-env-vars="ENABLE_AUTONOMOUS_PROVISIONING=true" \
    --quiet

echo ""
echo "🎉 DNA-Lang Autonomous Bio-Digital Platform has been deployed successfully!"
echo "==========================================================================="
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe dna-lang-platform --platform=managed --region=$REGION --format='value(status.url)')

echo "🌐 Platform URL: $SERVICE_URL"
echo "🧬 Evolution Engine: $SERVICE_URL (backend services auto-started)"
echo "📊 Cloud Console: https://console.cloud.google.com/run/detail/$REGION/dna-lang-platform/metrics?project=$PROJECT_ID"
echo "🗄️  Database: https://console.cloud.google.com/sql/instances/dnalang-genomic-db/overview?project=$PROJECT_ID"
echo "📡 Pub/Sub: https://console.cloud.google.com/cloudpubsub/topic/detail/dnalang-genomic-events?project=$PROJECT_ID"
echo ""
echo "✨ Your DNA-Lang Platform is now live with:"
echo "   • Living Digital Twins that evolve autonomously"
echo "   • Self-managing cloud infrastructure"
echo "   • Real-time genomic insights and analysis"
echo "   • AI-powered agents for cloud architecture optimization"
echo ""
echo "🚀 Ready to create self-evolving genomic organisms!"