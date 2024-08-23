resource "aws_iam_role_policy" "soil_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = aws_iam_role.soil_data_processing_recommendations_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "moisture_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = aws_iam_role.moisture_task_planner_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = aws_iam_role.soil_data_processing_recommendations_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "moisture_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = aws_iam_role.moisture_task_planner_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2"
      }
    ]
  })
}