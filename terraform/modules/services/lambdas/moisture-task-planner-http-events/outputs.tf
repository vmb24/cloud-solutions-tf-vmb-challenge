# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.moisture_task_planner_http_events_deployment.invoke_url
}

output "allow_s3_moisture_task_planner_http_events" {
  value = aws_lambda_permission.allow_s3_moisture_task_planner_http_events
}

output "moisture_task_planner_http_events_lambda_arn" {
  value = aws_lambda_function.moisture_task_planner_http_events.arn
}