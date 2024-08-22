resource "aws_lambda_function" "moisture_task_planner" {
  function_name = "moisture_task_planner"
  role          = var.moisture_task_planner_lambda_role_arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.moisture_task_planner.repository_url}:latest"

  environment {
    variables = {
      REKOGNITION_COLLECTION_ID = var.task_planner_faces_rekognition_collection_id
    }
  }
}

resource "aws_lambda_permission" "allow_iot" {
  statement_id  = "AllowExecutionFromIoT"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.moisture_task_planner.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = var.moisture_iot_rule_arn
}

# Permissão para o S3 invocar a função Lambda
resource "aws_lambda_permission" "allow_s3_moisture_task_planner" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.moisture_task_planner.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = var.task_planner_media_bucket_arn
}