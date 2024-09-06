# Permissão para o API Gateway invocar a função Lambda
resource "aws_lambda_permission" "air_moisture_apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.air_moisture_data_processing_recommendations.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.execution_arn}/*/*"
}