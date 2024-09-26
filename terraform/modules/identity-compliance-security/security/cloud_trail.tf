resource "aws_cloudtrail" "app_trail" {
  name                          = "agricultural-app-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_bucket.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.app_cloudtrail_key.arn
}

resource "aws_s3_bucket" "cloudtrail_bucket" {
  bucket        = "agricultural-app-cloudtrail-logs"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "cloudtrail_bucket_block" {
  bucket = aws_s3_bucket.cloudtrail_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}