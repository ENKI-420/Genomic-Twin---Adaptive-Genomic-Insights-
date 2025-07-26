variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "image_url" {
  description = "The container image URL for the DNA-Lang application"
  type        = string
  default     = "gcr.io/PROJECT_ID/genomic-twin-app:latest"
}