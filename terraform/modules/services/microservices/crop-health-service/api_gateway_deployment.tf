resource "aws_api_gateway_deployment" "crop_health_microservice" {
  depends_on = [
    aws_api_gateway_method.post_crop_health_service,
    aws_api_gateway_method.get_crop_health_service,
    aws_api_gateway_method.put_crop_health_service,
    aws_api_gateway_method.delete_crop_health_service,
    aws_api_gateway_integration.post_crop_health_service,
    aws_api_gateway_integration.get_crop_health_service,
    aws_api_gateway_integration.put_crop_health_service,
    aws_api_gateway_integration.delete_crop_health_service
  ]
  rest_api_id = aws_api_gateway_rest_api.crop_health_microservice.id
  stage_name  = "prod"
}