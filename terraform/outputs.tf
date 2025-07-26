output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.dnalang_app.status[0].url
}

output "database_connection_name" {
  description = "The connection name of the Cloud SQL instance"
  value       = google_sql_database_instance.dnalang_db.connection_name
}

output "pubsub_topic" {
  description = "The name of the Pub/Sub topic for genomic events"
  value       = google_pubsub_topic.genomic_events.name
}

output "artifact_registry_repository" {
  description = "The Artifact Registry repository URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.dnalang_repo.repository_id}"
}

output "service_account_email" {
  description = "The email of the service account used by Cloud Run"
  value       = google_service_account.dnalang_service_account.email
}

output "deployment_summary" {
  description = "Summary of the deployed DNA-Lang Genomic Twin infrastructure"
  value = {
    application_url    = google_cloud_run_service.dnalang_app.status[0].url
    database_instance  = google_sql_database_instance.dnalang_db.name
    pubsub_topic      = google_pubsub_topic.genomic_events.name
    container_registry = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.dnalang_repo.repository_id}"
    region            = var.region
    project_id        = var.project_id
  }
}