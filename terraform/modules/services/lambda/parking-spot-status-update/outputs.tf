# Saída do URL da API
# Output da URL do API Gateway
output "parking_spot_status_update_api_url" {
  description = "Base URL for Status API Gateway stage"
  value       = aws_api_gateway_deployment.parking_spot_status_deployment.invoke_url
}

output "parking_spot_status_update_lambda_arn" {
  value = aws_lambda_function.parking_spot_status_update.arn
}