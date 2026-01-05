# Terraform S3 Backend Configuration for QA Environment
# This file configures remote state storage in S3 with DynamoDB locking
#
# Prerequisites:
# - S3 bucket "tardigrade-terraform-state" must exist
# - DynamoDB table "tardigrade-terraform-locks" must exist
# - IAM permissions for S3 and DynamoDB access

terraform {
  backend "s3" {
    bucket         = "tardigrade-terraform-state"
    key            = "qa/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "tardigrade-terraform-locks"
  }
}
