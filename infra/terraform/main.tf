terraform {
  required_version = ">= 1.5"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "project" {
  type    = string
  default = "reimagined-carnival"
}

resource "local_file" "environment_info" {
  content  = "Project: ${var.project}\nEnvironment: ${var.environment}\n"
  filename = "${path.module}/env_${var.environment}.txt"
}

output "project" {
  value = var.project
}

output "environment" {
  value = var.environment
}
