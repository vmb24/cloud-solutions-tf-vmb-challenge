resource "aws_cloudwatch_event_rule" "farmer_update_rule" {
  name         = "FarmerUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["farmer_service"]
    detail-type = ["FarmerUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "farmer_update_target_soil_metrics" {
  rule      = aws_cloudwatch_event_rule.farmer_update_rule.name
  target_id = "soilMetricsTarget"
  arn       = var.sns_topic_soil_metrics_notifications_arn
}

resource "aws_cloudwatch_event_target" "farmer_update_target_weather" {
  rule      = aws_cloudwatch_event_rule.farmer_update_rule.name
  target_id = "weatherServiceTarget"
  arn       = var.sns_topic_weather_notifications_arn
}
