# Permissões para o API Gateway invocar a função Lambda
resource "aws_lambda_permission" "apigw_lambda_status_permission" {
  statement_id  = "AllowAPIGatewayInvokeStatus"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.parking_spot_status_update.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.parking_spot_status_api.execution_arn}/*/*"
}