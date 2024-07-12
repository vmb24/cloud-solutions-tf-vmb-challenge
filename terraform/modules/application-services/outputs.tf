output "api_url" {
  value = "${aws_api_gateway_deployment.deployment.invoke_url}/metrics"
}

output "execution_arn_api_gateway" {
  value = aws_api_gateway_rest_api.api.execution_arn
}