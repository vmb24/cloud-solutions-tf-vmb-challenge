resource "aws_ecs_cluster" "terrafarming_website_cluster" {
  name = "${var.ecs_website_service_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  configuration {
    execute_command_configuration {
      kms_key_id = var.kms_key_current_arn
      logging    = "OVERRIDE"

      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = var.cloudwatch_log_group_website_container_name
      }
    }
  }
}