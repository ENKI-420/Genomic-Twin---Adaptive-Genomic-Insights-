# Configuration settings for oncology AI platform
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.oncology.ai"

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT = "your-gcp-project-id"
GOOGLE_CLOUD_REGION = "us-central1"

# BigQuery Configuration
BIGQUERY_DATASET = "genomic_data"
CRISPR_BLAST_TABLE = "genomic_data.crispr_blast_index"
TISSUE_DELIVERY_TABLE = "genomic_data.tissue_delivery"

# Authentication settings
GOOGLE_APPLICATION_CREDENTIALS = None  # Path to service account JSON file
REQUIRE_AUTHENTICATION = True
