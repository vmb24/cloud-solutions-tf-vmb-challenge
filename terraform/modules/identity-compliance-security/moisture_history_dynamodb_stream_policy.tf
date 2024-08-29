resource "aws_iam_role_policy" "dynamodb_stream_policy" {
  name = "dynamodb_stream_policy"
  role = aws_iam_role.moisture_task_planner_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:DescribeStream",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:ListStreams",
          "dynamodb:Query"
        ]
        Resource = [
          var.dynamodb_table_moisture_history_stream_arn,
          var.dynamodb_table_moisture_history_arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem"
        ]
        Resource = var.dynamodb_table_task_plans_arn
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      }
    ]
  })
}
