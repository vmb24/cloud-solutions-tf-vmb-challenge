# Deployment da API Gateway
resource "aws_api_gateway_deployment" "parking_spot_status_deployment" {
  depends_on = [
    aws_api_gateway_integration.update_status_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.parking_spot_status_api.id
  stage_name  = "prod"
}