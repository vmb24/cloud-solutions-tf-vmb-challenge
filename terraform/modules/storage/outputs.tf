output "website_bucket_name" {
  value = aws_s3_bucket.website_bucket.bucket
}

output "website_bucket_regional_domain_name" {
  value = aws_s3_bucket.website_bucket.bucket_regional_domain_name
}

output "website_bucket_id" {
  value = aws_s3_bucket.website_bucket.id
}

output "task_planner_media_bucket_arn" {
  value = aws_s3_bucket.task_planner_media.arn
}

output "tf_state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.id
  description = "The name of the S3 bucket"
}