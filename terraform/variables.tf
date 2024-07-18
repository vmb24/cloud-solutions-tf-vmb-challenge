variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "account_id" {
  type    = string
  default = "590184100199"
}

# ----- NETWORK ------

variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "A list of CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "A list of CIDR blocks for the private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "availability_zones" {
  description = "A list of availability zones in the region"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# ------ COMPUTE ------
# ECR & ECS
variable "llm_soil_metrics_repository_name" {
  description = "The name of the ECR Terrafarming repository"
  type        = string
  default     = "llm-soil-metrics"
}

variable "key_name" {
  description = "The name of the key vms"
  type        = string
  default     = "vockey"
}

# S3
variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default = "terrafarming-metrics-data-storage"
}

variable "environment" {
  description = "The environment name (e.g., dev, prod)"
  type        = string
  default = "prod"
}