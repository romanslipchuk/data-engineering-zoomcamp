variable "credentials" {
  description = "My Credentials"
  default     = "../delearnproject20240121-dfb8fb0d184b.json"
}
variable "project" {
  description = "Project in GCP"
  default     = "delearnproject20240121"
}

variable "location" {
  description = "Location"
  default     = "EU"
}

variable "region" {
  description = "Progect region"
  default     = "europe-north1"
}

variable "bq_dataset_name" {
  description = "My BigQuerry Dataset"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My Storage BUcket Name"
  default     = "delearnproject20240121_bucket"
}