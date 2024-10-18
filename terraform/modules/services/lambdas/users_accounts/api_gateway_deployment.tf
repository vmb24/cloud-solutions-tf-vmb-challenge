resource "aws_api_gateway_deployment" "users_accounts_deployement" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]

  rest_api_id = aws_api_gateway_rest_api.users_accounts_api.id
  stage_name  = "prod"
}