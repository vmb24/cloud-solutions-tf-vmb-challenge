resource "aws_appautoscaling_target" "website_scaling_target" {
  max_capacity       = 4
  min_capacity       = 2
  resource_id        = "service/${var.terrafarming_website_ecs_cluster_name}/${aws_ecs_service.website_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "website_scaling_policy" {
  name                   = "website-scaling-policy"
  policy_type            = "TargetTrackingScaling"
  resource_id            = aws_appautoscaling_target.website_scaling_target.resource_id
  scalable_dimension     = aws_appautoscaling_target.website_scaling_target.scalable_dimension
  service_namespace      = aws_appautoscaling_target.website_scaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 75.0

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}