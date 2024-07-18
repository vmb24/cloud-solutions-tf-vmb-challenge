resource "aws_cloudwatch_event_rule" "crop_health_update_rule" {
  name         = "CropHealthUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["crop_health_service"]
    detail-type = ["CropHealthUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "crop_health_update_target_farmer" {
  rule      = aws_cloudwatch_event_rule.crop_health_update_rule.name
  target_id = "farmerServiceTarget"
  arn       = var.sns_topic_farmer_notifications_arn
}

resource "aws_cloudwatch_event_target" "crop_health_update_target_greenhouse" {
  rule      = aws_cloudwatch_event_rule.crop_health_update_rule.name
  target_id = "greenhouseServiceTarget"
  arn       = var.sns_topic_greenhouse_notifications_arn
}
