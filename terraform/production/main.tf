# Terraform configuration for production environment
# Deploys to AWS with production-grade settings

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # S3 backend for state management
  # Uncomment and configure for your AWS account
  # backend "s3" {
  #   bucket         = "tardigrade-terraform-state"
  #   key            = "production/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "tardigrade-terraform-locks"
  # }
}

# AWS Provider configuration
provider "aws" {
  region = var.aws_region

  # OIDC authentication (recommended for CI/CD)
  # Uncomment when using GitHub Actions or GitLab CI with OIDC
  # assume_role {
  #   role_arn = "arn:aws:iam::${var.aws_account_id}:role/TerraformProductionRole"
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
  default     = "production"
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
#   cidr_block           = "10.0.0.0/16"
#   enable_dns_hostnames = true
#   enable_dns_support   = true
#
#   tags = {
#     Name = "${var.project_name}-${var.environment}-vpc"
#   }
# }

# Public Subnets (for ALB)
# resource "aws_subnet" "public" {
#   count                   = 2
#   vpc_id                  = aws_vpc.main.id
#   cidr_block              = "10.0.${count.index + 1}.0/24"
#   availability_zone       = data.aws_availability_zones.available.names[count.index]
#   map_public_ip_on_launch = true
#
#   tags = {
#     Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"
#   }
# }

# Private Subnets (for ECS, RDS)
# resource "aws_subnet" "private" {
#   count             = 2
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.${count.index + 10}.0/24"
#   availability_zone = data.aws_availability_zones.available.names[count.index]
#
#   tags = {
#     Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"
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

# ECS Service with Fargate
# resource "aws_ecs_service" "api" {
#   name            = "${var.project_name}-api"
#   cluster         = aws_ecs_cluster.main.id
#   task_definition = aws_ecs_task_definition.api.arn
#   desired_count   = 2
#   launch_type     = "FARGATE"
#
#   network_configuration {
#     subnets          = aws_subnet.private[*].id
#     security_groups  = [aws_security_group.ecs.id]
#     assign_public_ip = false
#   }
#
#   load_balancer {
#     target_group_arn = aws_lb_target_group.api.arn
#     container_name   = "api"
#     container_port   = 8000
#   }
# }

# Aurora PostgreSQL (Production)
# resource "aws_rds_cluster" "main" {
#   cluster_identifier     = "${var.project_name}-${var.environment}"
#   engine                 = "aurora-postgresql"
#   engine_mode            = "provisioned"
#   engine_version         = "15.4"
#   database_name          = "tardigrade"
#   master_username        = "admin"
#   master_password        = var.db_password
#   backup_retention_period = 7
#   preferred_backup_window = "03:00-04:00"
#   skip_final_snapshot    = false
#   deletion_protection    = true
#   storage_encrypted      = true
#
#   serverlessv2_scaling_configuration {
#     min_capacity = 1.0
#     max_capacity = 8.0
#   }
# }

# ElastiCache Redis (Production)
# resource "aws_elasticache_replication_group" "main" {
#   replication_group_id       = "${var.project_name}-${var.environment}"
#   description                = "Redis cluster for ${var.project_name}"
#   node_type                  = "cache.t3.small"
#   num_cache_clusters         = 2
#   automatic_failover_enabled = true
#   engine_version             = "7.0"
#   port                       = 6379
#   at_rest_encryption_enabled = true
#   transit_encryption_enabled = true
# }

# CloudWatch Log Group
# resource "aws_cloudwatch_log_group" "api" {
#   name              = "/tardigrade/${var.environment}/api"
#   retention_in_days = 30
# }

# CloudWatch Alarms
# resource "aws_cloudwatch_metric_alarm" "api_errors" {
#   alarm_name          = "${var.project_name}-${var.environment}-api-errors"
#   comparison_operator = "GreaterThanThreshold"
#   evaluation_periods  = 2
#   metric_name         = "5XXError"
#   namespace           = "AWS/ApplicationELB"
#   period              = 300
#   statistic           = "Sum"
#   threshold           = 10
#   alarm_description   = "API 5XX errors exceeded threshold"
# }

# Outputs
output "environment" {
  description = "Environment name"
  value       = var.environment
}
