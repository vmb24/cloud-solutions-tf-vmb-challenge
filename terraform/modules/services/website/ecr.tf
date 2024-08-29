resource "aws_ecr_repository" "tech4parking_website_repo" {
  name = "tech4parking-website-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}