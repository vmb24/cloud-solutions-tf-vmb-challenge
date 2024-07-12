resource "aws_ecr_repository" "repo" {
  name = var.llm_soil_metrics_repository_name
}