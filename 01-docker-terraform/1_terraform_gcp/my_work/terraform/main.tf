terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.6.0"
    }
  }
}

provider "google" {
  credentials = "../delearnproject20240121-dfb8fb0d184b.json"
  project     = "delearnproject20240121"
  region      = "europe-north1"
}

resource "google_storage_bucket" "demo_da_course" {
  name          = "delearnproject20240121_bucket"
  location      = "EU"
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