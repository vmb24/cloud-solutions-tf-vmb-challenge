output "dynamodb_table_task_plans_arn" {
  value = aws_dynamodb_table.task_plans.arn
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_state_lock.id
  description = "The name of the DynamoDB table"
}