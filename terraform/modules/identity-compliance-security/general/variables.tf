variable "aws_region" {}
variable "ecs_website_service_name" {}

variable "website_bucket_id" {}
variable "website_bucket_name" {}

# Processing Lambdas Role IDs
variable "air_moisture_data_processing_recommendations_lambda_role_id" {
  description = "The IAM role ID for the air moisture data processing recommendations Lambda"
  type        = string
}

variable "air_temperature_data_processing_recommendations_lambda_role_id" {
  description = "The IAM role ID for the air temperature data processing recommendations Lambda"
  type        = string
}

variable "brightness_data_processing_recommendations_lambda_role_id" {
  description = "The IAM role ID for the brightness data processing recommendations Lambda"
  type        = string
}

variable "soil_moisture_data_processing_recommendations_lambda_role_id" {
  description = "The IAM role ID for the soil moisture data processing recommendations Lambda"
  type        = string
}

variable "soil_temperature_data_processing_recommendations_lambda_role_id" {
  description = "The IAM role ID for the soil temperature data processing recommendations Lambda"
  type        = string
}

# Task Planner Lambdas Role IDs
variable "air_moisture_task_planner_lambda_role_id" {
  description = "The IAM role ID for the air moisture task planner Lambda"
  type        = string
}

variable "air_temperature_task_planner_lambda_role_id" {
  description = "The IAM role ID for the air temperature task planner Lambda"
  type        = string
}

variable "brightness_task_planner_lambda_role_id" {
  description = "The IAM role ID for the brightness task planner Lambda"
  type        = string
}

variable "soil_moisture_task_planner_lambda_role_id" {
  description = "The IAM role ID for the soil moisture task planner Lambda"
  type        = string
}

variable "soil_temperature_task_planner_lambda_role_id" {
  description = "The IAM role ID for the soil temperature task planner Lambda"
  type        = string
}