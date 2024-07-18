resource "aws_cloudwatch_event_rule" "soil_metrics_update_rule" {
  name         = "SoilMetricsUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["soil_metrics_service"]
    detail-type = ["SoilMetricsUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "soil_metrics_update_target_crop_health" {
  rule      = aws_cloudwatch_event_rule.soil_metrics_update_rule.name
  target_id = "cropHealthServiceTarget"
  arn       = var.sns_topic_crop_health_notifications_arn
}

resource "aws_cloudwatch_event_target" "soil_metrics_update_target_equipment_health" {
  rule      = aws_cloudwatch_event_rule.soil_metrics_update_rule.name
  target_id = "equipmentHealthServiceTarget"
  arn       = var.sns_topic_equipment_health_notifications_arn
}
