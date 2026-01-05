# Terraform configuration for local development environment
# This configuration is for local development and testing purposes

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Local backend for development
  backend "local" {
    path = "terraform.tfstate"
  }
}

# AWS Provider configuration
# For local development, uses AWS credentials from environment or ~/.aws/credentials
provider "aws" {
  region = var.aws_region

  # Uncomment for LocalStack or other local AWS emulators
  # skip_credentials_validation = true
  # skip_metadata_api_check     = true
  # skip_requesting_account_id  = true
  # endpoints {
  #   dynamodb = "http://localhost:4566"
  #   s3       = "http://localhost:4566"
  #   sqs      = "http://localhost:4566"
  # }

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

# Local development resources are typically managed via Docker Compose
# This file serves as a template for AWS resource definitions

# Example: DynamoDB table for local testing (when using LocalStack)
# resource "aws_dynamodb_table" "example" {
#   name           = "${var.project_name}-${var.environment}-example"
#   billing_mode   = "PAY_PER_REQUEST"
#   hash_key       = "id"
#
#   attribute {
#     name = "id"
#     type = "S"
#   }
#
#   tags = {
#     Name = "${var.project_name}-${var.environment}-example"
#   }
# }
