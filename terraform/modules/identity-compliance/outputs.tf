output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_role.arn
}

output "iam_role_lambda_exec_arn" {
  value = aws_iam_role.lambda_exec.arn
}

output "amplify_mobile_service_role_arn" {
  value = aws_iam_role.amplify_mobile_service_role.arn
}