variable "aws_region" {}
variable "ecs_website_service_name" {}
variable "website_bucket_id" {}
variable "website_bucket_name" {}
variable task_planner_media_bucket_arn {}
variable kinesis_video_stream_task_planner_video_arn {}
variable dynamodb_table_task_plans_arn {}

variable "dynamodb_table_agricultural_moisture_recommendations_arn" {}

variable "ai_agricultural_soil_moisture_recommendations_tabledb_stream_arn" {}

variable "soil_moisture_history_dynamodb_table_arn" {}
variable "soil_moisture_averages_dynamodb_table__arn" {}

variable "soil_moisture_history_dynamodb_table_stream_arn" {}
