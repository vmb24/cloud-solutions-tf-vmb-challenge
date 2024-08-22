# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.moisture_task_planner_deployment.invoke_url
}

output "allow_s3_moisture_task_planner" {
  value = aws_lambda_permission.allow_s3_moisture_task_planner
}

output "moisture_task_planner_lambda_arn" {
  value = aws_lambda_function.moisture_task_planner.arn
}