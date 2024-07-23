resource "aws_api_gateway_deployment" "greenhouse_microservice" {
  depends_on = [
    aws_api_gateway_method.post_greenhouse_service,
    aws_api_gateway_method.get_greenhouse_service,
    aws_api_gateway_method.put_greenhouse_service,
    aws_api_gateway_method.delete_greenhouse_service,
    aws_api_gateway_integration.post_greenhouse_service,
    aws_api_gateway_integration.get_greenhouse_service,
    aws_api_gateway_integration.put_greenhouse_service,
    aws_api_gateway_integration.delete_greenhouse_service
  ]
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  stage_name  = "prod"
}