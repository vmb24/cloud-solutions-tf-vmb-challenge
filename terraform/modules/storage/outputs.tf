output "website_bucket_name" {
  value = aws_s3_bucket.website_bucket.bucket
}

output "website_bucket_regional_domain_name" {
  value = aws_s3_bucket.website_bucket.bucket_regional_domain_name
}

output "website_bucket_id" {
  value = aws_s3_bucket.website_bucket.id
}

output "logging_bucket_name" {
  value = aws_s3_bucket.logging_bucket.bucket
}

output "logging_bucket_arn" {
  value = aws_s3_bucket.logging_bucket.arn
}

# output "image_analysis_bucket_name" {
#   value = aws_s3_bucket.images_bucket.bucket
# }

# output "mobile_bucket_name" {
#   value = aws_s3_bucket.mobile_bucket.bucket
# }
