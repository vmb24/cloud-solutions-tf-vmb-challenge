data "aws_caller_identity" "soil_temperature_processing_data_current_caller_identity" {}

resource "aws_iam_role" "soil_temperature_task_planner_lambda_role" {
  name = "soil_temperature_task_planner_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          "Service": [
            "lambda.amazonaws.com",
            "apigateway.amazonaws.com"
          ]
        }
      }
    ]
  })
}

# Política IAM para a função Lambda
resource "aws_iam_role_policy" "soil_temperature_task_planner_lambda_policy" {
  name = "soil_task_planner_lambda_policy"
  role = aws_iam_role.soil_temperature_task_planner_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Scan",
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:UpdateItem",
        ]
        Resource = "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.soil_temperature_processing_data_current_caller_identity.account_id}:table/*"
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
      },
      {
        Effect = "Allow"
        Action = [
          "iot:GetThingShadow",
          "iot:UpdateThingShadow",
          "iot:DeleteThingShadow"
        ]
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.soil_temperature_processing_data_current_caller_identity.account_id}:thing/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "soil_temperature_task_planner_lambda_policy" {
  role       = aws_iam_role.soil_temperature_task_planner_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Permissão para o Rekognition acessar o S3 (se necessário)
# resource "aws_iam_role_policy_attachment" "rekognition_s3_access" {
#   role       = aws_iam_role.temperature_task_planner_lambda_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
# }