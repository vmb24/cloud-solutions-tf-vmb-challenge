resource "aws_s3_bucket" "website_bucket" {
  bucket = "website-bucket-${random_id.bucket_id.hex}"

  tags = {
    Name        = "website-bucket-${random_id.bucket_id.hex}"
    Environment = var.environment
  }
}