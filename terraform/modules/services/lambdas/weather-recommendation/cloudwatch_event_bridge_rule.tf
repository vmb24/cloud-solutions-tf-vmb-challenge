resource "aws_cloudwatch_event_rule" "weather_recommendation_rule" {
  name         = "WeatherRecommendationRule"
  event_bus_name = var.cloudwatch_event_bus_name
  event_pattern = jsonencode({
    source = ["weather_recommendation_lambda"]
    detail-type = ["WeatherRecommendation"]
  })
}

resource "aws_cloudwatch_event_target" "weather_recommendation_target_farmer" {
  rule      = aws_cloudwatch_event_rule.weather_recommendation_rule.name
  target_id = "farmerServiceTarget"
  arn       = var.sns_topic_farmer_notifications_arn
}
