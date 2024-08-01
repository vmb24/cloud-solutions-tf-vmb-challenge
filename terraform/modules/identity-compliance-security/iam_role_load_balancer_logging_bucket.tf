resource "aws_iam_role_policy" "lb_logging_policy" {
  name   = "lb-logging-policy"
  role   = aws_iam_role.lb_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ],
        Resource = "${var.load_balancer_logging_bucket_arn}/*"
      }
    ]
  })
}