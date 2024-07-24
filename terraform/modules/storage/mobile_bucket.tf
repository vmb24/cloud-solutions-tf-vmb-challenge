# resource "aws_s3_bucket" "mobile_bucket" {
#   bucket = "mobile-app-bucket-${random_id.bucket_id.hex}"

#   tags = {
#     Name        = "mobile-app-bucket-${random_id.bucket_id.hex}"
#     Environment = var.environment
#   }
# }