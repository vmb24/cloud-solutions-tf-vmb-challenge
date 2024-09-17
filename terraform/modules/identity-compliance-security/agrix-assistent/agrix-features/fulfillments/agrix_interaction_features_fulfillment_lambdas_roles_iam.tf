# Role IAM para as funções Lambda
# ESSA PRÁTICA NÃO É RECOMENDADA! CADA FUNÇÃO DEVE TER SUAS PRÓPRIAS PERMISSÕES
resource "aws_iam_role" "agrix_interaction_features_fulfillment_lambda_role" {
  name = "agrix_interaction_features_fulfillment_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Política IAM para acesso ao DynamoDB
resource "aws_iam_role_policy" "dynamodb_access" {
  name = "dynamodb_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:dynamodb:*:*:table/*"
      }
    ]
  })
}

# Política IAM para acesso ao Amazon Polly
resource "aws_iam_role_policy" "polly_access" {
  name = "polly_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "polly:SynthesizeSpeech"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# Política IAM para acesso ao Amazon Rekognition
resource "aws_iam_role_policy" "rekognition_access" {
  name = "rekognition_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "rekognition:DetectLabels",
          "rekognition:RecognizeText"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# Política IAM para acesso ao Amazon SageMaker
resource "aws_iam_role_policy" "sagemaker_access" {
  name = "sagemaker_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sagemaker:InvokeEndpoint"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# Política IAM para acesso ao AWS IoT
resource "aws_iam_role_policy" "iot_access" {
  name = "iot_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "iot:Publish",
          "iot:Receive",
          "iot:Subscribe"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:iot:*:*:topic/*"
      }
    ]
  })
}

# Política IAM para acesso ao Amazon S3 (caso necessário para armazenamento de dados ou arquivos)
resource "aws_iam_role_policy" "s3_access" {
  name = "s3_access"
  role = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::your-bucket-name",
          "arn:aws:s3:::your-bucket-name/*"
        ]
      }
    ]
  })
}

# Anexar a política de execução básica do Lambda
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.agrix_interaction_features_fulfillment_lambda_role.name
}