# Production Environment Terraform Configuration
# DNA-Lang Platform - Production Infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  
  backend "gcs" {
    bucket = "dna-lang-terraform-state-prod"
    prefix = "terraform/state"
  }
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "dna-lang-prod"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

# Provider Configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# Production VPC with strict security
resource "google_compute_network" "prod_vpc" {
  name                    = "dna-lang-prod-vpc"
  auto_create_subnetworks = false
  
  # Enable flow logs for security monitoring
  enable_logging = true
}

resource "google_compute_subnetwork" "prod_subnet" {
  name          = "dna-lang-prod-subnet"
  ip_cidr_range = "10.1.0.0/24"
  region        = var.region
  network       = google_compute_network.prod_vpc.id
  
  # Enable private Google access
  private_ip_google_access = true
  
  # Enable flow logs
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud NAT for outbound internet access
resource "google_compute_router" "prod_router" {
  name    = "dna-lang-prod-router"
  region  = var.region
  network = google_compute_network.prod_vpc.id
}

resource "google_compute_router_nat" "prod_nat" {
  name                               = "dna-lang-prod-nat"
  router                             = google_compute_router.prod_router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

# Firewall rules - restrictive for production
resource "google_compute_firewall" "prod_allow_internal" {
  name    = "dna-lang-prod-allow-internal"
  network = google_compute_network.prod_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["10.1.0.0/24"]
  target_tags   = ["dna-lang-prod"]
}

# BigQuery dataset for genomic data
resource "google_bigquery_dataset" "genomic_data" {
  dataset_id    = "genomic_data_prod"
  friendly_name = "DNA-Lang Genomic Data Production"
  description   = "Production genomic analysis data"
  location      = "US"

  # Enable customer-managed encryption
  default_encryption_configuration {
    kms_key_name = google_kms_crypto_key.genomic_key.id
  }
  
  # Access control
  access {
    role          = "OWNER"
    user_by_email = "dna-lang-prod-admin@company.com"
  }
}

# KMS key for encryption
resource "google_kms_key_ring" "genomic_keyring" {
  name     = "dna-lang-genomic-keyring"
  location = "global"
}

resource "google_kms_crypto_key" "genomic_key" {
  name     = "dna-lang-genomic-key"
  key_ring = google_kms_key_ring.genomic_keyring.id
  
  rotation_period = "7776000s"  # 90 days
}

# Cloud Storage bucket for genomic files
resource "google_storage_bucket" "genomic_files" {
  name     = "dna-lang-genomic-files-prod"
  location = "US"
  
  # Security configurations
  uniform_bucket_level_access = true
  
  encryption {
    default_kms_key_name = google_kms_crypto_key.genomic_key.id
  }
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
}

# IAM binding for production service account
resource "google_service_account" "prod_app_sa" {
  account_id   = "dna-lang-prod-app"
  display_name = "DNA-Lang Production Application Service Account"
}

resource "google_project_iam_member" "prod_genomics_viewer" {
  project = var.project_id
  role    = "roles/genomics.viewer"
  member  = "serviceAccount:${google_service_account.prod_app_sa.email}"
}