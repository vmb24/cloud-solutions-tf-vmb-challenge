# resource "aws_s3_bucket_policy" "load_balancer_logging_bucket_policy" {
#   bucket = var.load_balancer_logging_bucket_id

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid    = ""
#         Effect = "Allow"
#         Principal = "*"
#         Action   = "s3:PutObject"
#         Resource = "${var.load_balancer_logging_bucket_arn}/load-balancer-logs/*"
#         Condition = {
#           StringEquals = {
#             "aws:UserAgent" = "AWS-ELB-Logs"
#           }
#         }
#       }
#     ]
#   })
# }