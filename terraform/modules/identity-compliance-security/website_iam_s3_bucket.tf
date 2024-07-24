# resource "aws_s3_bucket_policy" "logging_bucket_policy" {
#   bucket = var.website_bucket_name

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid    = "AllowCloudFrontServicePrincipal"
#         Effect = "Allow"
#         Principal = {
#           Service = "cloudfront.amazonaws.com"
#         }
#         Action   = "s3:GetObject"
#         Resource = "${var.logging_bucket_arn}/*"
#       }
#     ]
#   })
# }
