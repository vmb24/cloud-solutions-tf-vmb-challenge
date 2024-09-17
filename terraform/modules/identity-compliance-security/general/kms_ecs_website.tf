resource "aws_kms_key" "current" {
  description             = "${var.ecs_website_service_name}-ecs kms key"
  deletion_window_in_days = 7
}

resource "aws_cloudwatch_log_group" "current" {
  name = "${var.ecs_website_service_name}-ecs"
}