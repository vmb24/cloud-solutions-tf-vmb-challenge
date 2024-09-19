output "website_bucket_name" {
  value = aws_s3_bucket.website_bucket.bucket
}

output "website_bucket_regional_domain_name" {
  value = aws_s3_bucket.website_bucket.bucket_regional_domain_name
}

output "website_bucket_id" {
  value = aws_s3_bucket.website_bucket.id
}

output "tf_state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.id
}

output "website_efs_id" {
  value = aws_efs_file_system.website_efs.id
}