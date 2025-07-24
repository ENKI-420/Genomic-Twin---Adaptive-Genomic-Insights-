# GCP Organization Deployment Guide
# DNA-Lang Platform - Environment Setup and Deployment

## Overview

This guide explains how to deploy the DNA-Lang platform using the mandated GCP organization folder structure that enforces organizational policies, manages access control at scale, and logically organizes resources.

## Prerequisites

1. GCP Organization with appropriate permissions
2. Terraform >= 1.0
3. Google Cloud SDK
4. Appropriate IAM permissions for each environment

## Environment Setup

### 1. Set Environment Variable

```bash
# For production deployment
export DNA_LANG_ENV=production

# For staging deployment  
export DNA_LANG_ENV=staging

# For development deployment
export DNA_LANG_ENV=development
```

### 2. Configure GCP Projects

Create separate GCP projects for each environment:

```bash
# Production
gcloud projects create dna-lang-prod --organization=YOUR_ORG_ID

# Staging
gcloud projects create dna-lang-staging --organization=YOUR_ORG_ID

# Development
gcloud projects create dna-lang-dev --organization=YOUR_ORG_ID
```

### 3. Apply Organization Policies

```bash
# Apply organization-wide policies
gcloud resource-manager org-policies set-policy \
  gcp-organization/resource-policies/organization-policies.yaml \
  --organization=YOUR_ORG_ID
```

### 4. Deploy Infrastructure

#### Production Environment

```bash
cd gcp-organization/terraform/prod
terraform init
terraform plan -var="project_id=dna-lang-prod"
terraform apply
```

#### Development Environment

```bash
cd gcp-organization/terraform/dev  
terraform init
terraform plan -var="project_id=dna-lang-dev"
terraform apply
```

### 5. Configure IAM Policies

```bash
# Apply production IAM policies
gcloud projects set-iam-policy dna-lang-prod \
  gcp-organization/iam-policies/prod-iam-policy.yaml

# Apply development IAM policies  
gcloud projects set-iam-policy dna-lang-dev \
  gcp-organization/iam-policies/dev-iam-policy.yaml
```

## Security Controls

### Production Environment

- **Encryption**: Customer-managed encryption keys (CMEK)
- **Network**: Private VPC with VPC Flow Logs enabled
- **Access**: MFA required, IP whitelisting enabled
- **Monitoring**: Full audit logging, Security Command Center enabled
- **Backup**: Daily backups with 90-day retention

### Staging Environment

- **Encryption**: Google-managed encryption
- **Network**: Private VPC, moderate firewall rules
- **Access**: MFA optional, broader access for testing
- **Monitoring**: Selective audit logging
- **Backup**: Weekly backups with 30-day retention

### Development Environment

- **Encryption**: Google-managed encryption
- **Network**: Public access allowed for development
- **Access**: No MFA required, broad developer access
- **Monitoring**: Minimal logging
- **Backup**: No automated backups
- **Features**: Auto-shutdown, synthetic data only

## Access Control Matrix

| Role | Production | Staging | Development |
|------|-----------|---------|-------------|
| Admin | Owner (MFA) | Editor | Editor |
| Developer | No Access | Viewer | Editor |
| Data Scientist | Viewer | Viewer | Editor |
| QA Team | No Access | Viewer | Viewer |
| Security Team | Viewer | Viewer | Viewer |

## Resource Organization

```
GCP Organization
├── dna-lang-prod (Production)
│   ├── VPC: dna-lang-prod-vpc
│   ├── BigQuery: genomic_data_prod
│   ├── Storage: dna-lang-genomic-files-prod
│   └── IAM: Strict controls with MFA
├── dna-lang-staging (Staging)  
│   ├── VPC: dna-lang-staging-vpc
│   ├── BigQuery: genomic_data_staging
│   ├── Storage: dna-lang-genomic-files-staging
│   └── IAM: Moderate controls
└── dna-lang-dev (Development)
    ├── VPC: dna-lang-dev-vpc
    ├── BigQuery: genomic_data_dev
    ├── Storage: dna-lang-genomic-files-dev
    └── IAM: Relaxed controls
```

## Environment Isolation

The folder structure prevents unauthorized access between environments through:

1. **Project Isolation**: Each environment uses separate GCP projects
2. **Network Segregation**: Isolated VPCs with environment-specific firewall rules  
3. **IAM Separation**: Environment-specific service accounts and IAM policies
4. **Resource Tagging**: Mandatory labels for environment identification
5. **Policy Enforcement**: Organization policies enforced at folder level

## Monitoring and Compliance

### Production Monitoring
- Cloud Audit Logs: All services
- Security Command Center: Enabled
- Data Loss Prevention: Enabled
- Vulnerability Scanning: Enabled

### Compliance Features
- HIPAA compliance configuration
- GDPR compliance settings
- Data residency controls
- Encryption at rest and in transit

## Application Configuration

The application automatically detects the environment and applies appropriate configurations:

```python
from environment_config import config

# Automatically uses environment-specific settings
project_id = config.project_id  # dna-lang-{environment}
security_level = config.security_level  # STRICT/MODERATE/RELAXED
requires_mfa = config.requires_mfa  # True for production
```

## Cost Optimization

### Development Environment
- Auto-shutdown schedules (weekdays 6 PM - 8 AM)
- Automatic resource cleanup after 30 days
- Budget alerts and spending controls

### Production Environment  
- Reserved instances for predictable workloads
- Coldline storage for long-term data retention
- Network optimization with Cloud CDN

## Troubleshooting

### Common Issues

1. **Permission Denied**: Verify IAM policies are correctly applied
2. **Environment Not Detected**: Check DNA_LANG_ENV environment variable
3. **Terraform Errors**: Ensure GCP projects exist and APIs are enabled
4. **Network Connectivity**: Verify VPC and firewall configurations

### Support Contacts

- **Production Issues**: production-support@company.com
- **Development Questions**: dev-team@company.com  
- **Security Concerns**: security-team@company.com