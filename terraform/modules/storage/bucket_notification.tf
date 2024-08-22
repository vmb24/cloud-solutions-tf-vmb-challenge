# Configuração de notificação do S3 para invocar a função Lambda
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.task_planner_media.id

  lambda_function {
    lambda_function_arn = var.moisture_task_planner_lambda_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "uploads/"
    filter_suffix       = ".json"
  }

  depends_on = [var.allow_s3_moisture_task_planner]
}