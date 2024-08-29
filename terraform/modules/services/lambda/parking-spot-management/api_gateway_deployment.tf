# Deployment do API Gateway
resource "aws_api_gateway_deployment" "parking_spot_management_deployment" {
  depends_on = [
    aws_api_gateway_integration.create_spot_integration,
    aws_api_gateway_integration.list_spots_integration,
    aws_api_gateway_integration.get_spot_integration,
    aws_api_gateway_integration.delete_spot_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  stage_name  = "prod"
}