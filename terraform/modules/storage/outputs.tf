output "website_bucket_name" {
  value = aws_s3_bucket.website_bucket.bucket
}

output "website_bucket_regional_domain_name" {
  value = aws_s3_bucket.website_bucket.bucket_regional_domain_name
}

output "website_bucket_id" {
  value = aws_s3_bucket.website_bucket.id
}

output "load_balancer_logging_bucket_id" {
  value = aws_s3_bucket.load_balancer_logging_bucket.id
}

output "load_balancer_logging_bucket_arn" {
  value = aws_s3_bucket.load_balancer_logging_bucket.arn
}

output "load_balancer_logging_bucket" {
  value = aws_s3_bucket.load_balancer_logging_bucket.bucket
}