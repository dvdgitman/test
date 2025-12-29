variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  default     = "prod"
}

variable "db_password" {
  description = "Password for the RDS instance"
  type        = string
  sensitive   = true # Terraform will redact this in CLI output
}

variable "rabbitmq_password" {
  description = "Password for RabbitMQ user"
  type        = string
  sensitive   = true
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate for HTTPS listener"
  type        = string
}
