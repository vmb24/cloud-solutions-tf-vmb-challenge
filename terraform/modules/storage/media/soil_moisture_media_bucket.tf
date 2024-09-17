# S3 Buckets
resource "aws_s3_bucket" "soil_moisture_media_bucket" {
  bucket = "soil_moisture_media_bucket"

  tags = {
    Name        = "soil_moisture_media_bucket"
    Environment = "Production"
  }
}

# S3 Bucket ACL
resource "aws_s3_bucket_acl" "soil_moisture_media_bucket_acl" {
  bucket = aws_s3_bucket.soil_moisture_media_bucket.id
  acl    = "private"
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "soil_moisture_media_bucket_versioning" {
  bucket = aws_s3_bucket.soil_moisture_media_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "soil_moisture_media_bucket_encryption" {
  bucket = aws_s3_bucket.soil_moisture_media_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}