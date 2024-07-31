# resource "aws_s3_bucket_policy" "logging_bucket_policy" {
#   bucket = var.website_bucket_name

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Sid    = "PublicReadForGetBucketObjects"
#         Effect = "Allow"
#         Principal = {
#           Service = "cloudfront.amazonaws.com"
#         }
#         Action   = "*"
#         Resource = "${var.cloudfront_logging_bucket_arn}/*"
#       }
#     ]
#   })
# }
