# DNA-Lang Deployment Guide

This guide covers production deployment of DNA-Lang organisms to Google Cloud Platform and other cloud providers.

## Prerequisites

Before deploying to production, ensure you have:

- **Google Cloud Project** with billing enabled
- **Required APIs** enabled (Cloud Run, Cloud SQL, Cloud Build, etc.)
- **Service Account** with appropriate permissions
- **Domain name** for custom URLs (optional)
- **SSL certificates** for HTTPS (recommended)

## Google Cloud Platform Deployment

### Quick Deploy (Recommended)

The fastest way to deploy DNA-Lang is using our one-click deployment:

1. **Click Deploy Button**:
   [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-in-cloud-shell.svg)](https://shell.cloud.google.com/cloudshell_open?git_repo=https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-&tutorial=README.md&shellonly=true)

2. **Follow Setup Wizard**:
   ```bash
   # The setup script will guide you through:
   # - Project configuration
   # - API enablement
   # - Service account creation
   # - Resource provisioning
   # - SSL certificate setup
   ```

3. **Access Your Deployment**:
   - Dashboard: `https://your-project-id-dashboard-abc123-uc.a.run.app`
   - API: `https://your-project-id-api-abc123-uc.a.run.app`

### Manual Deployment

For more control over the deployment process:

#### Step 1: Environment Setup

```bash
# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export SERVICE_ACCOUNT="dna-lang-service@${PROJECT_ID}.iam.gserviceaccount.com"

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project $PROJECT_ID
```

#### Step 2: Enable Required APIs

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  sql-component.googleapis.com \
  pubsub.googleapis.com \
  secretmanager.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com
```

#### Step 3: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create dna-lang-service \
  --display-name="DNA-Lang Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/cloudsql.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/pubsub.admin"
```

#### Step 4: Deploy Infrastructure with Terraform

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan \
  -var="project_id=${PROJECT_ID}" \
  -var="region=${REGION}" \
  -var="service_account=${SERVICE_ACCOUNT}"

# Apply infrastructure
terraform apply -auto-approve
```

#### Step 5: Deploy Application Services

```bash
# Build and deploy backend services
gcloud builds submit \
  --config=cloudbuild-backend.yaml \
  --substitutions=_PROJECT_ID=$PROJECT_ID,_REGION=$REGION

# Build and deploy frontend dashboard
gcloud builds submit \
  --config=cloudbuild-frontend.yaml \
  --substitutions=_PROJECT_ID=$PROJECT_ID,_REGION=$REGION
```

#### Step 6: Configure DNS and SSL

```bash
# Map custom domain (optional)
gcloud run domain-mappings create \
  --service=dna-lang-dashboard \
  --domain=dashboard.yourdomain.com \
  --region=$REGION

# SSL certificates are automatically provisioned
```

## Multi-Cloud Deployment

### Amazon Web Services (AWS)

Deploy DNA-Lang organisms to AWS using ECS and Lambda:

```bash
# Configure AWS credentials
aws configure

# Deploy using our AWS CloudFormation template
aws cloudformation create-stack \
  --stack-name dna-lang-platform \
  --template-body file://aws/cloudformation-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production \
  --capabilities CAPABILITY_IAM
```

### Microsoft Azure

Deploy to Azure using Container Instances and Functions:

```bash
# Login to Azure
az login

# Create resource group
az group create --name dna-lang-rg --location eastus

# Deploy using ARM template
az deployment group create \
  --resource-group dna-lang-rg \
  --template-file azure/arm-template.json \
  --parameters environment=production
```

## Environment Configuration

### Production Environment Variables

Create a `.env.production` file with production settings:

```bash
# Environment
NODE_ENV=production
ENVIRONMENT=production

# Google Cloud Platform
GCP_PROJECT_ID=your-production-project
GCP_REGION=us-central1
GCP_SERVICE_ACCOUNT_KEY=/path/to/service-account-key.json

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dnalang_prod
DATABASE_SSL=true
DATABASE_POOL_SIZE=20

# API Configuration
API_BASE_URL=https://api.yourdomain.com
CORS_ORIGINS=https://dashboard.yourdomain.com,https://yourdomain.com

# Security
JWT_SECRET=your-super-secret-jwt-key
API_RATE_LIMIT=1000
ENABLE_HTTPS_REDIRECT=true

# Monitoring
ENABLE_PROMETHEUS_METRICS=true
LOG_LEVEL=info
SENTRY_DSN=https://your-sentry-dsn

# Evolution Engine
MAX_CONCURRENT_ORGANISMS=50
EVOLUTION_CYCLE_INTERVAL=30000
MUTATION_SAFETY_CHECKS=true
```

### Security Configuration

#### SSL/TLS Configuration

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'dna-lang-api'
      - '--image=gcr.io/$PROJECT_ID/dna-lang-api:$BUILD_ID'
      - '--platform=managed'
      - '--region=us-central1'
      - '--allow-unauthenticated'
      - '--port=3000'
      - '--cpu=2'
      - '--memory=4Gi'
      - '--max-instances=100'
      - '--set-env-vars=NODE_ENV=production'
      - '--service-account=dna-lang-service@$PROJECT_ID.iam.gserviceaccount.com'
```

#### IAM and Access Control

```bash
# Create minimal IAM policy for organisms
cat > organism-policy.json << EOF
{
  "bindings": [
    {
      "role": "roles/run.invoker",
      "members": ["serviceAccount:organism-runner@${PROJECT_ID}.iam.gserviceaccount.com"]
    },
    {
      "role": "roles/cloudsql.client",
      "members": ["serviceAccount:organism-runner@${PROJECT_ID}.iam.gserviceaccount.com"]
    }
  ]
}
EOF

gcloud projects set-iam-policy $PROJECT_ID organism-policy.json
```

## Monitoring and Observability

### Prometheus Metrics

DNA-Lang exposes Prometheus metrics for monitoring:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dna-lang-api'
    static_configs:
      - targets: ['api.yourdomain.com:443']
    scheme: https
    metrics_path: '/metrics'
    
  - job_name: 'dna-lang-organisms'
    static_configs:
      - targets: ['organism-1.yourdomain.com:443']
    scheme: https
    metrics_path: '/organism/metrics'
```

### Key Metrics to Monitor

- **Organism Health**: `organism_consciousness`, `organism_fitness`, `organism_stability`
- **Evolution Performance**: `mutation_success_rate`, `generation_duration`, `transcendence_rate`
- **Infrastructure**: `cloud_run_instances`, `database_connections`, `pubsub_message_latency`
- **Application**: `api_request_duration`, `api_error_rate`, `websocket_connections`

### Grafana Dashboard

Import our pre-built Grafana dashboard:

```bash
# Download dashboard configuration
curl -o dna-lang-dashboard.json \
  https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/monitoring/grafana-dashboard.json

# Import to Grafana
curl -X POST \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @dna-lang-dashboard.json \
  http://your-grafana-instance/api/dashboards/db
```

## Backup and Disaster Recovery

### Database Backups

```bash
# Automated daily backups
gcloud sql backups create \
  --instance=dna-lang-db \
  --description="Daily backup $(date +%Y-%m-%d)"

# Point-in-time recovery setup
gcloud sql instances patch dna-lang-db \
  --backup-start-time=02:00 \
  --retained-backups-count=30
```

### Organism State Backups

```bash
# Backup organism states to Cloud Storage
gsutil -m cp -r gs://dna-lang-organisms-backup/$(date +%Y-%m-%d)/ \
  /local/backup/organisms/

# Automated backup script
cat > backup-organisms.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
BUCKET="gs://dna-lang-organisms-backup"

# Export organism states
kubectl get organisms -o yaml > organisms-${DATE}.yaml

# Upload to Cloud Storage
gsutil cp organisms-${DATE}.yaml ${BUCKET}/${DATE}/

# Cleanup local files
rm organisms-${DATE}.yaml
EOF

chmod +x backup-organisms.sh
```

### Disaster Recovery Plan

1. **RTO (Recovery Time Objective)**: 4 hours
2. **RPO (Recovery Point Objective)**: 1 hour
3. **Multi-region deployment** for high availability
4. **Automated failover** using Cloud Load Balancer

## Scaling Configuration

### Horizontal Scaling

```yaml
# kubernetes/organism-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dna-lang-organisms
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dna-lang-organisms
  template:
    metadata:
      labels:
        app: dna-lang-organisms
    spec:
      containers:
      - name: organism-runner
        image: gcr.io/PROJECT_ID/dna-lang-organism:latest
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: dna-lang-organisms-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dna-lang-organisms
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Vertical Scaling

```bash
# Scale Cloud Run services
gcloud run services update dna-lang-api \
  --cpu=4 \
  --memory=8Gi \
  --max-instances=100 \
  --region=us-central1

# Scale Cloud SQL instance
gcloud sql instances patch dna-lang-db \
  --tier=db-custom-8-32768 \
  --storage-size=1000GB
```

## Cost Optimization

### Resource Right-sizing

```bash
# Analyze resource utilization
gcloud monitoring metrics list --limit=100 | grep compute

# Right-size based on utilization data
gcloud compute instances set-machine-type INSTANCE_NAME \
  --machine-type=e2-standard-4 \
  --zone=us-central1-a
```

### Budget Alerts

```bash
# Create budget alert
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="DNA-Lang Production Budget" \
  --budget-amount=5000USD \
  --threshold-rules=percent=90,spend-basis=current-spend \
  --notification-channels=NOTIFICATION_CHANNEL_ID
```

## Troubleshooting

### Common Issues

#### Organism Failed to Start

```bash
# Check Cloud Run logs
gcloud logs read --service=dna-lang-organisms --limit=50

# Check organism-specific logs
kubectl logs -l app=organism-abc123 --tail=100
```

#### Database Connection Issues

```bash
# Test database connectivity
gcloud sql connect dna-lang-db --user=postgres

# Check connection pool status
psql -h HOST -U USER -d DATABASE -c "SELECT * FROM pg_stat_activity;"
```

#### Evolution Engine Stuck

```bash
# Restart evolution engine
kubectl rollout restart deployment/evolution-engine

# Check for deadlocks
kubectl exec -it evolution-engine-pod -- node debug-evolution.js
```

### Performance Tuning

#### Database Optimization

```sql
-- Optimize database for organism queries
CREATE INDEX CONCURRENTLY idx_organisms_status ON organisms(status);
CREATE INDEX CONCURRENTLY idx_mutations_timestamp ON mutations(created_at);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM organisms WHERE status = 'active';
```

#### Cache Configuration

```bash
# Configure Redis for caching
gcloud redis instances create dna-lang-cache \
  --size=5 \
  --region=us-central1 \
  --tier=standard

# Update application configuration
export REDIS_URL=redis://REDIS_HOST:6379
```

## Security Hardening

### Network Security

```bash
# Create VPC with private subnets
gcloud compute networks create dna-lang-vpc --subnet-mode=custom

gcloud compute networks subnets create dna-lang-subnet \
  --network=dna-lang-vpc \
  --range=10.1.0.0/24 \
  --region=us-central1
```

### Secret Management

```bash
# Store secrets in Secret Manager
echo -n "super-secret-jwt-key" | \
  gcloud secrets create jwt-secret --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding jwt-secret \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

### Security Scanning

```bash
# Container vulnerability scanning
gcloud container images scan IMAGE_URL

# Binary authorization
gcloud container binauthz policy import policy.yaml
```

## Maintenance

### Regular Updates

```bash
# Update DNA-Lang platform
git pull origin main
docker build -t gcr.io/$PROJECT_ID/dna-lang-api:latest .
gcloud run deploy dna-lang-api --image=gcr.io/$PROJECT_ID/dna-lang-api:latest

# Update organism dependencies
npm audit fix
npm update
```

### Health Checks

```bash
# API health check
curl -f https://api.yourdomain.com/health || exit 1

# Database health check
gcloud sql instances describe dna-lang-db --format="value(state)"

# Organism health check
kubectl get pods -l app=dna-lang-organisms
```

## Support

For deployment support:

- **Documentation**: [docs.dnalang.dev/deployment](https://docs.dnalang.dev/deployment)
- **Enterprise Support**: [enterprise@dnalang.dev](mailto:enterprise@dnalang.dev)
- **Community Forum**: [community.dnalang.dev](https://community.dnalang.dev)
- **Professional Services**: Available for complex deployments