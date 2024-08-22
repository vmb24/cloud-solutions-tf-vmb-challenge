resource "aws_lambda_function" "soil_data_processing_recommendations" {
  function_name = "soil_data_processing_recommendations"
  role          = var.soil_data_processing_recommendations_lambda_role_arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.soil_data_processing_recommendations.repository_url}:latest"
}

resource "aws_lambda_permission" "allow_iot" {
  statement_id  = "AllowExecutionFromIoT"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.soil_data_processing_recommendations.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = var.moisture_iot_rule_arn
}
