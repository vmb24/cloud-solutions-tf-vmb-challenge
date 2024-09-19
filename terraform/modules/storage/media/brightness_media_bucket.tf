# S3 Buckets
resource "aws_s3_bucket" "brightness_media_bucket" {
  bucket = "brightness_media_bucket"

  tags = {
    Name        = "brightness_media_bucket"
    Environment = "Production"
  }
}

# S3 Bucket ACL
resource "aws_s3_bucket_acl" "brightness_media_bucket_acl" {
  bucket = aws_s3_bucket.brightness_media_bucket.id
  acl    = "private"
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "brightness_media_bucket_versioning" {
  bucket = aws_s3_bucket.brightness_media_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "brightness_media_bucket_encryption" {
  bucket = aws_s3_bucket.brightness_media_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}