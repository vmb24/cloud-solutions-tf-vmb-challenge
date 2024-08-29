variable "aws_region" {
  type    = string
  default = "us-east-1"
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
variable "cognito_stage_name" {
  description = "Cognito stage name"
  type        = string
  default     = "production"
}

variable "route53_record_www_record_name" {
  description = "Record Name"
  type        = string
  default     = "www.vagasasaservice.com.br"
}


variable "http_certificate" {
  description = "HTTPS Certificate"
  type        = string
  sensitive   = true
  default     = "arn:aws:acm:us-east-1:021891598585:certificate/9133f5bf-141f-44b8-93fe-d11d5d704ba4"
}

variable "cognito_service_name" {
  description = "Cognito service name"
  type        = string
  default     = "website-cognito"
}

# variable "autoscaling_instance_type" {
#   description = "Autoscaling instance type"
#   type = string
#   default = "t2.micro"
# }

variable "key_name" {
  description = "The name of the key vms"
  type        = string
  default     = "vockey"
}

# S3
variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default     = "tech4parking-metrics-data-storage"
}

variable "environment" {
  description = "The environment name (e.g., dev, prod)"
  type        = string
  default     = "prod"
}

## IDENTITY - COMPLIANCE - SECURITY ##
variable "ecs_website_service_name" {
  description = "The ECS name"
  type        = string
  default     = "tech4parking-website"
}

## DELIVERY CONTENT - WEBSITE ##
# variable "acm_certificate_cert_arn" {
#   description = "HTTPS Certificate"
#   type        = string
#   default     = "arn:aws:acm:us-east-1:590184100199:certificate/58370164-61ab-4d3c-a048-f7e4ac2fa7ec"
# }

