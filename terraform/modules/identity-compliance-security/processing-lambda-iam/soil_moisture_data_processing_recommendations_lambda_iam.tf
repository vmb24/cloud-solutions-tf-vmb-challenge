data "aws_caller_identity" "soil_moisture_processing_data_current_caller_identity" {}

resource "aws_iam_role" "soil_moisture_data_processing_recommendations_lambda_role" {
  name = "soil_moisture_data_processing_recommendations_lambda"

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
resource "aws_iam_role_policy" "soil_moisture_data_processing_recommendations_lambda_policy" {
  name = "soil_moisture_data_processing_recommendations_lambda_policy"
  role = aws_iam_role.soil_moisture_data_processing_recommendations_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:UpdateItem",  
          "dynamodb:Scan"    
        ]
        Resource = "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.soil_moisture_processing_data_current_caller_identity.account_id}:table/*"
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
          "bedrock:*"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iot:GetThingShadow",
          "iot:UpdateThingShadow",
          "iot:DeleteThingShadow"
        ]
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.soil_moisture_processing_data_current_caller_identity.account_id}:thing/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "soil_moisture_data_processing_recommendations_lambda_policy_attachment" {
  role       = aws_iam_role.soil_moisture_data_processing_recommendations_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}