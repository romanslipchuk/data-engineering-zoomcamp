terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.6.0"
    }
  }
}

provider "google" {
  credentials = var.credentials
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "demo_da_course" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "data_talks_demo_dataset" {
  dataset_id    = var.bq_dataset_name
  friendly_name = "test"
  description   = "This is a test description"
  location      = var.location
}