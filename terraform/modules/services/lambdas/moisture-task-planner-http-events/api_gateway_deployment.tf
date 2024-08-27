# Deployment da API Gateway
resource "aws_api_gateway_deployment" "moisture_task_planner_http_events_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_task_plan,
    aws_api_gateway_integration.lambda_images,
    aws_api_gateway_integration.lambda_videos,
    aws_api_gateway_integration.lambda_generate_task_plan
  ]

  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  stage_name  = "prod"
}