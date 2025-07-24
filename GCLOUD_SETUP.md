# Google Cloud Authentication Setup

This document explains how to set up Google Cloud authentication for the Genomic Twin platform.

## Overview

The platform integrates with Google Cloud services including:
- **BigQuery**: For genomic data analysis and CRISPR off-target searches
- **Cloud Storage**: For storing large genomic datasets (future feature)
- **Cloud AI/ML**: For advanced genomic predictions (future feature)

## Authentication Methods

### Method 1: gcloud CLI (Recommended for Development)

1. **Install Google Cloud SDK**
   ```bash
   # Download and install from: https://cloud.google.com/sdk/docs/install
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL  # Restart shell
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Verify Authentication**
   ```bash
   python gcloud_cli.py status
   ```

### Method 2: Service Account (Recommended for Production)

1. **Create Service Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to IAM & Admin > Service Accounts
   - Create a new service account with BigQuery permissions

2. **Download Credentials**
   - Download the JSON key file
   - Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

3. **Set Project ID**
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   ```

### Method 3: Environment Variables

Set credentials directly as environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type": "service_account", ...}'
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

## Using the CLI Tool

The platform includes a CLI tool for managing authentication:

```bash
# Check authentication status
python gcloud_cli.py status

# Authenticate (interactive)
python gcloud_cli.py login

# Show setup instructions
python gcloud_cli.py setup

# Configure project
python gcloud_cli.py config --project YOUR_PROJECT_ID
```

## Using in the Application

### Streamlit Interface

1. Launch the application:
   ```bash
   streamlit run app.py
   ```

2. In the sidebar, you'll see a "Google Cloud Authentication" section
3. Check status and authenticate as needed

### Programmatic Usage

```python
from modules.gcloud_auth import gcloud_login, is_authenticated

# Check authentication
if not is_authenticated():
    # Authenticate
    success = gcloud_login()
    if success:
        print("Authentication successful!")
    else:
        print("Authentication failed")

# Use CRISPR analysis with BigQuery
from modules.crispr_ai import crispr_feasibility
result = crispr_feasibility("BRCA1")
```

## Required Permissions

Your Google Cloud account/service account needs these permissions:
- `bigquery.datasets.get`
- `bigquery.tables.get`
- `bigquery.jobs.create`
- `bigquery.data.get`

## Troubleshooting

### Common Issues

1. **"Google Cloud SDK not installed"**
   - Install Google Cloud dependencies: `pip install google-cloud-bigquery google-auth`

2. **"Authentication failed"**
   - Run `gcloud auth login` manually
   - Check that your account has necessary permissions
   - Verify project ID is correct

3. **"BigQuery not available"**
   - Install BigQuery client: `pip install google-cloud-bigquery`
   - Check network connectivity

### Getting Help

- Check authentication status: `python gcloud_cli.py status`
- View setup instructions: `python gcloud_cli.py setup`
- Check logs for detailed error messages

## Features Enabled by Authentication

Once authenticated, you can use:

1. **CRISPR Analysis**: Advanced off-target search using BigQuery
2. **Genomic Insights**: Large-scale genomic database queries
3. **Clinical Trial Matching**: Enhanced trial discovery with cloud data
4. **Future Features**: ML-powered genomic predictions and cloud storage

## Security Notes

- Never commit service account keys to version control
- Use environment variables for credentials in production
- Regularly rotate service account keys
- Follow principle of least privilege for permissions