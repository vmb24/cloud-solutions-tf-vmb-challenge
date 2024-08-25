resource "aws_iam_role" "moisture_task_planner_lambda_role" {
  name = "moisture_task_planner_lambda"

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
resource "aws_iam_role_policy" "moisture_task_planner_lambda_policy" {
  name = "task-planner-lambda-policy"
  role = aws_iam_role.moisture_task_planner_lambda_role.id

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
          var.task_planner_media_bucket_arn,
          "${var.task_planner_media_bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kinesisvideo:GetDataEndpoint",
          "kinesisvideo:PutMedia"
        ]
        Resource = var.kinesis_video_stream_task_planner_video_arn
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = [
          var.dynamodb_table_task_plans_arn, 
          var.dynamodb_table_moisture_history_arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "rekognition:DetectLabels",
          "rekognition:DetectFaces",
          "rekognition:SearchFacesByImage",
          "rekognition:IndexFaces",
          "rekognition:ListFaces",
          "rekognition:DeleteFaces",
          "rekognition:SearchFaces",
          "rekognition:CompareFaces",
          "rekognition:DetectText"
        ]
        Resource = "*"
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

resource "aws_iam_role_policy_attachment" "moisture_task_planner_lambda_policy" {
  role       = aws_iam_role.moisture_task_planner_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Permissão para o Rekognition acessar o S3 (se necessário)
# resource "aws_iam_role_policy_attachment" "rekognition_s3_access" {
#   role       = aws_iam_role.moisture_task_planner_lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
# }