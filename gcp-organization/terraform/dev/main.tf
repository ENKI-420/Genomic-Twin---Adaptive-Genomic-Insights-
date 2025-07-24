# Development Environment Terraform Configuration
# DNA-Lang Platform - Development Infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  
  backend "gcs" {
    bucket = "dna-lang-terraform-state-dev"
    prefix = "terraform/state"
  }
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "dna-lang-dev"
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

# Development VPC with relaxed security
resource "google_compute_network" "dev_vpc" {
  name                    = "dna-lang-dev-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "dev_subnet" {
  name          = "dna-lang-dev-subnet"
  ip_cidr_range = "10.3.0.0/24"
  region        = var.region
  network       = google_compute_network.dev_vpc.id
  
  # Disable private Google access for development
  private_ip_google_access = false
}

# Firewall rules - permissive for development
resource "google_compute_firewall" "dev_allow_all" {
  name    = "dna-lang-dev-allow-all"
  network = google_compute_network.dev_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080", "3000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["dna-lang-dev"]
}

# BigQuery dataset for development
resource "google_bigquery_dataset" "genomic_data_dev" {
  dataset_id    = "genomic_data_dev"
  friendly_name = "DNA-Lang Genomic Data Development"
  description   = "Development genomic analysis data - synthetic data only"
  location      = "US"
  
  # No encryption for development
  # Use default Google-managed encryption
  
  # Access control - more permissive
  access {
    role          = "OWNER"
    group_by_email = "dna-lang-developers@company.com"
  }
}

# Cloud Storage bucket for development
resource "google_storage_bucket" "genomic_files_dev" {
  name     = "dna-lang-genomic-files-dev"
  location = "US"
  
  # Basic configurations for development
  uniform_bucket_level_access = true
  
  # Auto-delete objects after 30 days
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# IAM binding for development service account
resource "google_service_account" "dev_app_sa" {
  account_id   = "dna-lang-dev-app"
  display_name = "DNA-Lang Development Application Service Account"
}

resource "google_project_iam_member" "dev_genomics_editor" {
  project = var.project_id
  role    = "roles/genomics.editor"
  member  = "serviceAccount:${google_service_account.dev_app_sa.email}"
}

# Cost control - automatic shutdown schedules
resource "google_compute_instance_schedule_policy" "dev_shutdown" {
  name        = "dev-auto-shutdown"
  description = "Automatically shutdown development instances"
  
  vm_start_schedule {
    schedule = "0 8 * * MON-FRI"  # Start at 8 AM weekdays
  }
  
  vm_stop_schedule {
    schedule = "0 18 * * MON-FRI"  # Stop at 6 PM weekdays
  }
  
  time_zone = "America/New_York"
}