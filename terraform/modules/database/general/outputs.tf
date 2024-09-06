# TFState Table
output "dynamodb_tfstate_table_name" {
  value       = aws_dynamodb_table.terraform_state_lock.id
  description = "The name of the DynamoDB table"
}