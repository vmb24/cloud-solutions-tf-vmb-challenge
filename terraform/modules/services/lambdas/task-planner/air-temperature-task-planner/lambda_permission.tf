# Permissão para API Gateway invocar Lambda
resource "aws_lambda_permission" "air_temperature_apigw_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.air_temperature_task_planner.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.air_temperature_task_planner_api.execution_arn}/*/*"
}