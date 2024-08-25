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
output "soil_data_processing_recommendations_lambda_role_arn" {
  value = aws_iam_role.soil_data_processing_recommendations_lambda_role.arn
}

output "moisture_task_planner_lambda_role_arn" {
  value = aws_iam_role.moisture_task_planner_lambda_role.arn
}

output "moisture_task_planner_http_events_lambda_role_arn" {
  value = aws_iam_role.moisture_task_planner_http_events_lambda_role.arn
}