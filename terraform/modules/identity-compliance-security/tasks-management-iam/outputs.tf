# Task planner lambdas ARN
output "tasks_management_lambda_role_arn" {
  value = aws_iam_role.tasks_management_lambda_role.arn
}

# Lambdas names
output "tasks_management_lambda_role_name" {
  value = aws_iam_role.tasks_management_lambda_role.name
}