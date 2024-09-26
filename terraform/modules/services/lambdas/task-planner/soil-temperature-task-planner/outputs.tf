# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.soil_temperature_task_planner_deployment.invoke_url
}

output "soil_temperature_task_planner_apigw_lambda_invoke_permission" {
  value = aws_lambda_permission.soil_temperature_task_planner_allow_apigateway_invoke
}

output "soil_temperature_task_planner_lambda_arn" {
  value = aws_lambda_function.soil_temperature_task_planner.arn
}