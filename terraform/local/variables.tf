# Input variables for local development environment

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tardigrade"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

# Database configuration
variable "database_name" {
  description = "Name of the database"
  type        = string
  default     = "tardigrade_local"
}

variable "database_port" {
  description = "Database port"
  type        = number
  default     = 5432
}

# Redis configuration
variable "redis_port" {
  description = "Redis port"
  type        = number
  default     = 6379
}

# API configuration
variable "api_port" {
  description = "API server port"
  type        = number
  default     = 8000
}
