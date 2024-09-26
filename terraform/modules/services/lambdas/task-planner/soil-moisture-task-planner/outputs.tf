# Saída do URL da API
output "api_url" {
  value = aws_api_gateway_deployment.soil_moisture_task_planner_deployment.invoke_url
}

output "soil_moisture_task_planner_apigw_invoke_lambda_permission" {
  value = aws_lambda_permission.soil_moisture_task_planner_allow_apigateway_invoke
}

output "soil_moisture_task_planner_lambda_arn" {
  value = aws_lambda_function.soil_moisture_task_planner.arn
}