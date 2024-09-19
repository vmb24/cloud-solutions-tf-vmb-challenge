# Task planner lambdas ARN
output "tasks_results_merge_lambda_role_arn" {
  value = aws_iam_role.tasks_results_merge_lambda_role.arn
}

# Lambdas names
output "tasks_results_merge_lambda_role_name" {
  value = aws_iam_role.tasks_results_merge_lambda_role.name
}