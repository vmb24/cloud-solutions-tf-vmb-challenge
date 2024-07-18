resource "aws_cloudwatch_event_rule" "weather_update_rule" {
  name         = "WeatherUpdateRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["weather_service"]
    detail-type = ["WeatherUpdate"]
  })
}

resource "aws_cloudwatch_event_target" "weather_update_target_recommendation" {
  rule      = aws_cloudwatch_event_rule.weather_update_rule.name
  target_id = "weatherRecommendationTarget"
  arn       = var.sns_topic_weather_recommendation_notifications_arn
}

resource "aws_cloudwatch_event_target" "weather_update_target_crop_health" {
  rule      = aws_cloudwatch_event_rule.weather_update_rule.name
  target_id = "cropHealthServiceTarget"
  arn       = var.sns_topic_crop_health_notifications_arn
}
