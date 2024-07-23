resource "aws_ecr_repository" "terrafarming_website_repo" {
  name = "terrafarming-website-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}