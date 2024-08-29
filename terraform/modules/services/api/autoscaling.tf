resource "aws_appautoscaling_target" "farmer_target_autoscaling" {
  max_capacity       = 4
  min_capacity       = 1
  resource_id        = "service/${var.terrafarming_microservices_ecs_cluster_name}/${aws_ecs_service.farmer_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "target_tracking_policy" {
  name               = "target_tracking_policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.farmer_target_autoscaling.resource_id
  scalable_dimension = aws_appautoscaling_target.farmer_target_autoscaling.scalable_dimension
  service_namespace  = aws_appautoscaling_target.farmer_target_autoscaling.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 75.0
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 300
  }
}