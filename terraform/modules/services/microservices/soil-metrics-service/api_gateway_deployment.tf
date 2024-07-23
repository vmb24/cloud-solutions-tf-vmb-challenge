resource "aws_api_gateway_deployment" "soil_metrics_microservice" {
  depends_on = [
    aws_api_gateway_method.post_soil_metrics_service,
    aws_api_gateway_method.get_soil_metrics_service,
    aws_api_gateway_method.put_soil_metrics_service,
    aws_api_gateway_method.delete_soil_metrics_service,
    aws_api_gateway_integration.post_soil_metrics_service,
    aws_api_gateway_integration.get_soil_metrics_service,
    aws_api_gateway_integration.put_soil_metrics_service,
    aws_api_gateway_integration.delete_soil_metrics_service
  ]
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  stage_name  = "prod"
}