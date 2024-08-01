resource "aws_s3_bucket" "load_balancer_logging_bucket" {
  bucket = "load-balancer-logging-bucket-${random_id.bucket_id.hex}"

  tags = {
    Name        = "load-balancer-logging-bucket-${random_id.bucket_id.hex}"
    Environment = var.environment
  }
}
  
resource "aws_s3_bucket_ownership_controls" "load_balancer_logging_bucket_ownership_controls" {
  bucket = aws_s3_bucket.load_balancer_logging_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "load_balancer_bucket_public_access_block" {
  bucket = aws_s3_bucket.load_balancer_logging_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "load_balancer_logging_bucket_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.load_balancer_logging_bucket_ownership_controls,
    aws_s3_bucket_public_access_block.load_balancer_bucket_public_access_block,
  ]

  bucket = aws_s3_bucket.load_balancer_logging_bucket.id
  acl    = "private"
}