resource "aws_cloudwatch_event_rule" "image_analyzed_rule" {
  name         = "ImageAnalyzedRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["image_analysis_lambda"]
    detail-type = ["ImageAnalyzed"]
  })
}

resource "aws_cloudwatch_event_target" "image_analyzed_target_crop_health" {
  rule      = aws_cloudwatch_event_rule.image_analyzed_rule.name
  target_id = "cropHealthServiceTarget"
  arn       = var.sns_topic_crop_health_notifications_arn
}
