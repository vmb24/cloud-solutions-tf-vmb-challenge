resource "aws_iam_role" "lb_role" {
  name = "load-balancer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "elasticloadbalancing.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "Load Balancer Role"
  }
}