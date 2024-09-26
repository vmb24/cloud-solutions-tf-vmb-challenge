# S3 Buckets
resource "aws_s3_bucket" "air_moisture_media_bucket" {
  bucket = "air-moisture-media-bucket"

  tags = {
    Name        = "air-moisture-media-bucket"
    Environment = "Production"
  }
}

# S3 Bucket Ownership Controls
resource "aws_s3_bucket_ownership_controls" "air_moisture_media_bucket_ownership" {
  bucket = aws_s3_bucket.air_moisture_media_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# S3 Bucket ACL
resource "aws_s3_bucket_acl" "air_moisture_media_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.air_moisture_media_bucket_ownership]

  bucket = aws_s3_bucket.air_moisture_media_bucket.id
  acl    = "private"
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "air_moisture_media_bucket_versioning" {
  bucket = aws_s3_bucket.air_moisture_media_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "air_moisture_media_bucket_encryption" {
  bucket = aws_s3_bucket.air_moisture_media_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}