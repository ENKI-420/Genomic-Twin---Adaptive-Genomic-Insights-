# DNA-Lang Genomic Twin Deployment Guide

This guide provides detailed instructions for deploying the DNA-Lang Genomic Twin platform on Google Cloud Platform using three different approaches.

## Prerequisites

- Google Cloud Project with billing enabled
- Basic familiarity with Google Cloud Console
- (Optional) gcloud CLI installed locally

## 🚀 Option 1: One-Click Cloud Shell Deployment

**Best for:** Quick demos, development environments, and first-time users.

### Steps:

1. **Click the Deploy Button**
   [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-in-cloud-shell.svg)](https://shell.cloud.google.com/cloudshell_open?git_repo=https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-&tutorial=README.md&shellonly=true)

2. **Run the Setup Script**
   ```bash
   chmod +x setup.sh && ./setup.sh
   ```

3. **Select Your Project**
   - The script will display available projects
   - Select using `fzf` (if available) or enter Project ID manually

4. **Wait for Deployment**
   - APIs will be enabled automatically
   - Infrastructure will be provisioned
   - Application will be built and deployed

5. **Access Your Application**
   - The script will output the Cloud Run service URL
   - Click the URL to access your DNA-Lang platform

### What Gets Deployed:
- Cloud Run service for the Streamlit application
- Cloud SQL PostgreSQL database for genomic data
- Pub/Sub topic for event processing
- Artifact Registry repository for container images
- IAM service accounts with minimal permissions

## 🏗️ Option 2: Terraform + Cloud Build (Production)

**Best for:** Production environments, CI/CD pipelines, and infrastructure management.

### Prerequisites:
- Google Cloud Project with Owner or Editor role
- Cloud Build API enabled

### Method A: Using Cloud Build Trigger

1. **Enable Required APIs**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable sourcerepo.googleapis.com
   ```

2. **Create Cloud Build Trigger**
   ```bash
   gcloud builds triggers import --source=cloudbuild-trigger.yaml
   ```

3. **Run the Trigger**
   - Go to Cloud Build > Triggers in Google Cloud Console
   - Find "dnalang-genomic-twin-deploy" trigger
   - Click "RUN" and provide required substitutions

### Method B: Manual Cloud Build

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
   cd Genomic-Twin---Adaptive-Genomic-Insights-
   ```

2. **Submit Build**
   ```bash
   gcloud builds submit --config=cloudbuild.yaml \
     --substitutions=_REGION=us-central1,_REPO_NAME=dnalang-repo
   ```

### Method C: Local Terraform

1. **Initialize Terraform**
   ```bash
   cd terraform
   terraform init
   ```

2. **Plan Deployment**
   ```bash
   terraform plan -var="project_id=YOUR_PROJECT_ID" \
     -var="region=us-central1" \
     -var="image_url=gcr.io/YOUR_PROJECT_ID/genomic-twin-app:latest"
   ```

3. **Apply Configuration**
   ```bash
   terraform apply -auto-approve \
     -var="project_id=YOUR_PROJECT_ID" \
     -var="region=us-central1" \
     -var="image_url=gcr.io/YOUR_PROJECT_ID/genomic-twin-app:latest"
   ```

## 🏪 Option 3: Google Cloud Marketplace (Future)

**Best for:** Enterprise deployments with integrated billing and support.

### Current Status:
This option is in preparation. The following components are ready:
- Terraform modules for marketplace deployment
- Parameter validation and configuration templates
- Documentation and support materials

### Timeline:
- Submit to Google Cloud Marketplace: Q2 2024
- Review and approval process: 2-4 weeks
- Public availability: Q3 2024

## 🔧 Configuration Options

### Environment Variables
Set these in Cloud Run or during deployment:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `PROJECT_ID` | Google Cloud Project ID | Auto-detected |
| `PUBSUB_TOPIC` | Event processing topic | `dnalang-genomic-events` |
| `PORT` | Application port | `8080` |

### Scaling Configuration
Modify in `terraform/main.tf`:

```hcl
metadata {
  annotations = {
    "autoscaling.knative.dev/maxScale" = "100"  # Max instances
    "autoscaling.knative.dev/minScale" = "0"    # Min instances
  }
}
```

### Database Configuration
Adjust in `terraform/main.tf`:

```hcl
settings {
  tier              = "db-f1-micro"    # Change for production
  availability_type = "REGIONAL"       # For high availability
  disk_size         = 100              # Increase for more storage
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```
   Error: Permission denied
   ```
   **Solution:** Ensure your account has Project Editor or Owner role

2. **API Not Enabled**
   ```
   Error: API not enabled
   ```
   **Solution:** Run the setup script or enable APIs manually:
   ```bash
   gcloud services enable run.googleapis.com cloudsql.googleapis.com
   ```

3. **Container Build Failed**
   ```
   Error: Failed to build container
   ```
   **Solution:** Check `cloudbuild.yaml` configuration and ensure Artifact Registry repository exists

4. **Database Connection Failed**
   ```
   Error: Could not connect to database
   ```
   **Solution:** Verify Cloud SQL instance is running and connection string is correct

### Validation Commands

```bash
# Check Cloud Run service
gcloud run services list --platform=managed

# Check Cloud SQL instance
gcloud sql instances list

# Check Pub/Sub topics
gcloud pubsub topics list

# Test application health
curl -f https://YOUR_SERVICE_URL/_stcore/health
```

## 🔄 Updates and Maintenance

### Updating the Application

1. **Using Cloud Build**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/genomic-twin-app:latest
   ```

2. **Deploy New Version**
   ```bash
   gcloud run deploy dnalang-genomic-twin \
     --image gcr.io/PROJECT_ID/genomic-twin-app:latest \
     --region us-central1
   ```

### Database Maintenance

1. **Backup Database**
   ```bash
   gcloud sql backups create --instance=dnalang-genomic-db
   ```

2. **Update Database Schema**
   - Connect to Cloud SQL instance
   - Run migration scripts
   - Test application functionality

## 📊 Monitoring and Observability

### Built-in Monitoring
- Cloud Run metrics (requests, latency, errors)
- Cloud SQL performance insights
- Pub/Sub message processing metrics

### Setting Up Alerts
```bash
# CPU utilization alert
gcloud alpha monitoring policies create --policy-from-file=monitoring/cpu-alert.yaml

# Error rate alert
gcloud alpha monitoring policies create --policy-from-file=monitoring/error-alert.yaml
```

### Logs Access
```bash
# Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Cloud SQL logs
gcloud logs read "resource.type=cloudsql_database" --limit=50
```

## 🔒 Security Best Practices

1. **Network Security**
   - Cloud Run service uses HTTPS by default
   - Cloud SQL uses private IP with SSL
   - IAM service accounts with minimal permissions

2. **Data Protection**
   - Database backups enabled
   - Encryption at rest and in transit
   - Audit logging enabled

3. **Access Control**
   - Use Google Cloud IAM for user access
   - Service accounts for application access
   - Regular access reviews

## 💰 Cost Optimization

### Resource Sizing
- **Development:** Use `db-f1-micro` for Cloud SQL
- **Production:** Use `db-n1-standard-1` or higher
- **Auto-scaling:** Set appropriate min/max instances

### Cost Monitoring
```bash
# Enable billing budget alerts
gcloud billing budgets create --billing-account=ACCOUNT_ID \
  --display-name="DNA-Lang Budget" \
  --budget-amount=100USD
```

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/issues)
- **Documentation:** [Project Wiki](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/wiki)
- **Community:** [Discussions](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/discussions)

## 📚 Additional Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)