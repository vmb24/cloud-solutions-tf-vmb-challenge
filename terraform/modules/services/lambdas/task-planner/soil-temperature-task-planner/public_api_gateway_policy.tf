resource "aws_api_gateway_rest_api_policy" "api_policy" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "execute-api:Invoke"
        Resource = "${aws_api_gateway_rest_api.soil_temperature_task_planner_api.execution_arn}/*/*/*"
      }
    ]
  })
}