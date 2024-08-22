output "dynamodb_table_task_plans_arn" {
  value = aws_dynamodb_table.task_plans.arn
}

output "dynamodb_table_average_moisture_arn" {
  value = aws_dynamodb_table.average_moisture.arn
}

output "dynamodb_tfstate_table_name" {
  value       = aws_dynamodb_table.terraform_state_lock.id
  description = "The name of the DynamoDB table"
}

output "average_moisture_tabledb_stream_arn" {
  value = aws_dynamodb_table.average_moisture.stream_arn
}