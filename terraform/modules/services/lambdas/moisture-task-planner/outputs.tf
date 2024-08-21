output "moisture_task_planner_lambda_arn" {
  value = aws_lambda_function.moisture_task_planner.arn
}

# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.moisture_task_planner_deployment.invoke_url
}