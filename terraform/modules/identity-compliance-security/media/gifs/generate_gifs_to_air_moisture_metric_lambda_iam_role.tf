resource "aws_iam_role" "generate_gifs_to_air_moisture_metric_lambda_role" {
  name = "generate_gifs_to_air_moisture_metric_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Política IAM para a função Lambda
resource "aws_iam_role_policy" "generate_gifs_to_air_moisture_metric_lambda_policy" {
  name = "soil_task_planner_lambda_policy"
  role = aws_iam_role.generate_gifs_to_air_moisture_metric_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.air_moisture_media_bucket_arn,
          "${var.air_moisture_media_bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:*"
        ]
        Resource = "*",
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "generate_gifs_to_air_moisture_metric_lambda_policy" {
  role       = aws_iam_role.generate_gifs_to_air_moisture_metric_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}