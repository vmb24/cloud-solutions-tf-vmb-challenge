data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda_function.zip"
  excludes    = ["lambda.tf", "variables.tf", "outputs.tf"]
}

resource "aws_lambda_function" "moisture_task_planner" {
  function_name    = "moisture_task_planner"
  role             = var.moisture_task_planner_lambda_role_arn
  handler          = "moisture_task_planner.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  architectures = ["x86_64"]

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