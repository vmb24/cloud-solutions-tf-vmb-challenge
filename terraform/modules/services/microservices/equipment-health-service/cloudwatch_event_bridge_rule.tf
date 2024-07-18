resource "aws_cloudwatch_event_rule" "equipment_health_update_rule" {
  name         = "EquipmentHealthUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["equipment_health_service"]
    detail-type = ["EquipmentHealthUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "equipment_health_update_target_farmer" {
  rule      = aws_cloudwatch_event_rule.equipment_health_update_rule.name
  target_id = "farmerServiceTarget"
  arn       = var.sns_topic_farmer_notifications_arn
}

resource "aws_cloudwatch_event_target" "equipment_health_update_target_soil_metrics" {
  rule      = aws_cloudwatch_event_rule.equipment_health_update_rule.name
  target_id = "soilMetricsServiceTarget"
  arn       = var.sns_topic_soil_metrics_notifications_arn
}
