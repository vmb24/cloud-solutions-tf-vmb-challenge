resource "aws_api_gateway_deployment" "weather_recommendation_deployment" {
  depends_on = [
    aws_api_gateway_method.post_method,
    aws_api_gateway_method.get_method,
    aws_api_gateway_integration.post_integration,
    aws_api_gateway_integration.get_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.weather_recommendation.id  # ID do API Gateway
  stage_name  = "prod"  # Nome do estágio para deployment

  variables = {
    "environment" = "production"
  }
}
