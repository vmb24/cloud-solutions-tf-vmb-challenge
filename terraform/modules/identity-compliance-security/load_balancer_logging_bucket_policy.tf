resource "aws_s3_bucket_policy" "lb_logs_policy" {
  bucket = var.load_balancer_logging_bucket_id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = "*",
        Action   = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ],
        Resource = "${var.load_balancer_logging_bucket_arn}/load-balancer-logs/*",
        Condition = {
          StringEquals = {
            "aws:referer" = "arn:aws:iam::590184100199:role/your-load-balancer-role"
          }
        }
      }
    ]
  })
}
