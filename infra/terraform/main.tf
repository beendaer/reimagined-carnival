terraform { required_version = ">= 1.5" }
variable "environment" { default = "staging" type = string }
variable "project" { default = "reimagined-carnival" type = string }
output "project" { value = var.project }
output "environment" { value = var.environment }
