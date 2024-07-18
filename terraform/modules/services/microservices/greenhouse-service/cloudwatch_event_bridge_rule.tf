resource "aws_cloudwatch_event_rule" "greenhouse_update_rule" {
  name         = "GreenhouseUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["greenhouse_service"]
    detail-type = ["GreenhouseUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "greenhouse_update_target_farmer" {
  rule      = aws_cloudwatch_event_rule.greenhouse_update_rule.name
  target_id = "farmerServiceTarget"
  arn       = var.sns_topic_farmer_notifications_arn
}
