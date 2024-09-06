# Task Planner Tables
output "ai_soil_moisture_task_plans_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_soil_moisture_task_plans.arn
}

output "ai_soil_temperature_task_plans_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_soil_temperature_task_plans.arn
}

output "ai_air_moisture_task_plans_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_air_moisture_task_plans.arn
}

output "ai_air_temperature_task_plans_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_air_temperature_task_plans.arn
}

output "ai_brightness_task_plans_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_brightness_task_plans
}