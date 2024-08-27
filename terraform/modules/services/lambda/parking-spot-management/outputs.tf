# Output da URL do API Gateway
output "parking_spot_management_api_url" {
  description = "Base URL for API Gateway stage"
  value       = aws_api_gateway_deployment.parking_spot_management_deployment.invoke_url
}

output "parking_spot_management_lambda_arn" {
  value = aws_lambda_function.parking_spot_management.arn
}