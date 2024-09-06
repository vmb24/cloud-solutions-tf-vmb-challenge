# S3 Buckets
resource "aws_s3_bucket" "media_buckets" {
  for_each = toset([
    "soil_moisture_media_bucket",
    "soil_temperature_media_bucket",
    "air_moisture_media_bucket",
    "air_temperature_media_bucket",
    "brightness_media_bucket"
  ])

  bucket = each.key

  tags = {
    Name        = each.key
    Environment = "Production"
  }
}

# S3 Bucket ACL
resource "aws_s3_bucket_acl" "bucket_acl" {
  for_each = aws_s3_bucket.media_buckets

  bucket = each.value.id
  acl    = "private"
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "bucket_versioning" {
  for_each = aws_s3_bucket.media_buckets

  bucket = each.value.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  for_each = aws_s3_bucket.media_buckets

  bucket = each.value.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}