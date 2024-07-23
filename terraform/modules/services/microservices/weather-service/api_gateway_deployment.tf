resource "aws_api_gateway_deployment" "weather_microservice" {
  depends_on = [
    aws_api_gateway_method.post_weather_service,
    aws_api_gateway_method.get_weather_service,
    aws_api_gateway_method.put_weather_service,
    aws_api_gateway_method.delete_weather_service,
    aws_api_gateway_integration.post_weather_service,
    aws_api_gateway_integration.get_weather_service,
    aws_api_gateway_integration.put_weather_service,
    aws_api_gateway_integration.delete_weather_service
  ]
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  stage_name  = "prod"
}