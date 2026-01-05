# Terraform configuration for QA environment
# Deploys to AWS with QA-specific settings

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend configuration is in backend.tf
}

# AWS Provider configuration
provider "aws" {
  region = var.aws_region

  # OIDC authentication (recommended for CI/CD)
  # Uncomment when using GitHub Actions or GitLab CI with OIDC
  # assume_role {
  #   role_arn = "arn:aws:iam::${var.aws_account_id}:role/TerraformQARole"
  # }

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

# Variables
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tardigrade"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "qa"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
  default     = ""
}

# VPC Configuration
# resource "aws_vpc" "main" {
#   cidr_block           = "10.1.0.0/16"
#   enable_dns_hostnames = true
#   enable_dns_support   = true
#
#   tags = {
#     Name = "${var.project_name}-${var.environment}-vpc"
#   }
# }

# ECS Cluster
# resource "aws_ecs_cluster" "main" {
#   name = "${var.project_name}-${var.environment}"
#
#   setting {
#     name  = "containerInsights"
#     value = "enabled"
#   }
# }

# Aurora PostgreSQL
# resource "aws_rds_cluster" "main" {
#   cluster_identifier     = "${var.project_name}-${var.environment}"
#   engine                 = "aurora-postgresql"
#   engine_mode            = "provisioned"
#   engine_version         = "15.4"
#   database_name          = "tardigrade"
#   master_username        = "admin"
#   master_password        = var.db_password
#   skip_final_snapshot    = true
#   deletion_protection    = false
#
#   serverlessv2_scaling_configuration {
#     min_capacity = 0.5
#     max_capacity = 2.0
#   }
# }

# ElastiCache Redis
# resource "aws_elasticache_cluster" "main" {
#   cluster_id           = "${var.project_name}-${var.environment}"
#   engine               = "redis"
#   node_type            = "cache.t3.micro"
#   num_cache_nodes      = 1
#   parameter_group_name = "default.redis7"
#   port                 = 6379
# }

# CloudWatch Log Group
# resource "aws_cloudwatch_log_group" "api" {
#   name              = "/tardigrade/${var.environment}/api"
#   retention_in_days = 7
# }

# Outputs
output "environment" {
  description = "Environment name"
  value       = var.environment
}
