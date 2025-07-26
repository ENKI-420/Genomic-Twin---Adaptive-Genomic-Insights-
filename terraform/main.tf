terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_services" {
  for_each = toset([
    "run.googleapis.com",
    "iam.googleapis.com",
    "cloudsql.googleapis.com",
    "pubsub.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
  ])
  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = false
}

# Artifact Registry repository for container images
resource "google_artifact_registry_repository" "dnalang_repo" {
  location      = var.region
  repository_id = "dnalang-repo"
  description   = "DNA-Lang Genomic Twin container repository"
  format        = "DOCKER"

  depends_on = [google_project_service.required_services]
}

# Cloud SQL instance for genomic data storage
resource "google_sql_database_instance" "dnalang_db" {
  name             = "dnalang-genomic-db"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 20

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        value = "0.0.0.0/0"
        name  = "all"
      }
    }
  }

  deletion_protection = false
  depends_on         = [google_project_service.required_services]
}

# Database and user
resource "google_sql_database" "genomic_twin_db" {
  name     = "genomic_twin_db"
  instance = google_sql_database_instance.dnalang_db.name
}

resource "google_sql_user" "dnauser" {
  name     = "dnauser"
  instance = google_sql_database_instance.dnalang_db.name
  password = "genomic_twin_2024"
}

# Pub/Sub topic for genomic event processing
resource "google_pubsub_topic" "genomic_events" {
  name = "dnalang-genomic-events"
  depends_on = [google_project_service.required_services]
}

resource "google_pubsub_subscription" "genomic_events_sub" {
  name  = "dnalang-genomic-events-sub"
  topic = google_pubsub_topic.genomic_events.name

  ack_deadline_seconds = 20
}

# Service account for Cloud Run
resource "google_service_account" "dnalang_service_account" {
  account_id   = "dnalang-genomic-twin-sa"
  display_name = "DNA-Lang Genomic Twin Service Account"
}

resource "google_project_iam_member" "dnalang_cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.dnalang_service_account.email}"
}

resource "google_project_iam_member" "dnalang_pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.dnalang_service_account.email}"
}

resource "google_project_iam_member" "dnalang_pubsub_subscriber" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.dnalang_service_account.email}"
}

# Cloud Run service
resource "google_cloud_run_service" "dnalang_app" {
  name     = "dnalang-genomic-twin"
  location = var.region

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"        = "10"
        "run.googleapis.com/cloudsql-instances"   = google_sql_database_instance.dnalang_db.connection_name
        "run.googleapis.com/execution-environment" = "gen2"
      }
    }

    spec {
      service_account_name = google_service_account.dnalang_service_account.email
      
      containers {
        image = var.image_url
        
        ports {
          container_port = 8080
        }

        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }

        env {
          name  = "DATABASE_URL"
          value = "postgresql://${google_sql_user.dnauser.name}:${google_sql_user.dnauser.password}@/${google_sql_database.genomic_twin_db.name}?host=/cloudsql/${google_sql_database_instance.dnalang_db.connection_name}"
        }

        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "PUBSUB_TOPIC"
          value = google_pubsub_topic.genomic_events.name
        }

        env {
          name  = "PORT"
          value = "8080"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.required_services]
}

# Allow unauthenticated access to the Cloud Run service
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.dnalang_app.name
  location = google_cloud_run_service.dnalang_app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}