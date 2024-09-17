data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda_function.zip"
  excludes    = ["lambda.tf", "variables.tf", "outputs.tf"]
}

resource "aws_lambda_function" "generate_gifs_to_brightness_metric" {
  function_name    = "generate_gifs_to_brightness_metric"
  role             = var.generate_gifs_to_brightness_metric_lambda_role_arn
  handler          = "generate_gifs_to_brightness_metric.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  architectures = ["x86_64"]
  # Aumentar o timeout (em segundos)
  timeout = 300  # 5 minutos, por exemplo

  # Aumentar a memória
  memory_size = 256  # em MB

  # environment {
  #   variables = {
  #     REKOGNITION_COLLECTION_ID = var.task_planner_faces_rekognition_collection_id
  #   }
  # }
}