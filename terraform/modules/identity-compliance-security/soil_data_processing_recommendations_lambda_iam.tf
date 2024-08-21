resource "aws_iam_role" "soil_data_processing_recommendations_lambda_role" {
  name = "soil_data_processing_recommendations_lambda"

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

resource "aws_iam_role_policy_attachment" "soil_data_processing_recommendations_lambda_policy" {
  role       = aws_iam_role.soil_data_processing_recommendations_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}