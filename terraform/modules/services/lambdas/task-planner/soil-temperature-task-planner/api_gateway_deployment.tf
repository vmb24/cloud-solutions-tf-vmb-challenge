resource "aws_api_gateway_deployment" "soil_temperature_task_planner_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_task_plan,
    aws_api_gateway_integration_response.get_task_plan_integration_response,
    aws_api_gateway_integration.options_integration,
    aws_api_gateway_integration_response.options_integration_response
  ]

  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  stage_name  = "prod"
}