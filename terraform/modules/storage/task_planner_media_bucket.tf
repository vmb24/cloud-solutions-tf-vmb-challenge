# S3 Bucket para armazenar imagens e vídeos
resource "aws_s3_bucket" "task_planner_media" {
  bucket = "task-planner-media-bucket"
}

# Permissão para o S3 Bucket
resource "aws_s3_bucket_public_access_block" "task_planner_media" {
  bucket = aws_s3_bucket.task_planner_media.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}