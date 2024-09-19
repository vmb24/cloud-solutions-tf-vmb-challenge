output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "iam_role_lambda_exec_arn" {
  value = aws_iam_role.lambda_exec.arn
}
output "kms_key_current_arn" {
  value = aws_kms_key.current.arn
}

output "ecs_task_execution_role_name" {
  value = aws_iam_role.ecs_task_execution_role.name
}

output "step_function_role_arn" {
  value = aws_iam_role.step_function_role.arn
}