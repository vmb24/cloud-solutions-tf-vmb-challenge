resource "aws_lambda_permission" "allow_apigw_post" {
  statement_id  = "AllowAPIGatewayInvokePOST"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.llm_metrics.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.execution_arn_api_gateway}/*/POST/metrics"
}

resource "aws_lambda_permission" "allow_apigw_get" {
  statement_id  = "AllowAPIGatewayInvokeGET"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.llm_metrics.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.execution_arn_api_gateway}/*/GET/metrics"
}