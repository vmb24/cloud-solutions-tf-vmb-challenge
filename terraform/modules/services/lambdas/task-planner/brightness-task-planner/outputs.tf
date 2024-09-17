# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.brightness_task_planner_deployment.invoke_url
}

output "allow_s3_brightness_task_planner" {
  value = aws_lambda_permission.brightness_apigw_lambda_permission
}

output "brightness_task_planner_lambda_arn" {
  value = aws_lambda_function.brightness_task_planner.arn
}