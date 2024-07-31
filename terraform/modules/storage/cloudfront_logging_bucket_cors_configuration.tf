resource "aws_s3_bucket_cors_configuration" "cloudfornt_logging_bucket_cors" {
  bucket = aws_s3_bucket.cloudfront_logging_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
  }
}