resource "aws_sns_topic" "website_alarms" {
  name = "website-alarms"
}

resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "high-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "TargetResponseTime"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Average"
  threshold           = "1"  # 1 segundo
  alarm_description   = "This metric monitors for high latency"
  alarm_actions       = [aws_sns_topic.website_alarms.arn]

  dimensions = {
    LoadBalancer = var.website_load_balancer_arn_suffix
    TargetGroup  = var.website_lb_target_arn_suffix
  }
}

resource "aws_cloudwatch_metric_alarm" "high_5xx_errors" {
  alarm_name          = "high-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Sum"
  threshold           = "10"  # 10 erros 5xx em 1 minuto
  alarm_description   = "This metric monitors for high 5xx error rates"
  alarm_actions       = [aws_sns_topic.website_alarms.arn]

  dimensions = {
    LoadBalancer = var.website_load_balancer_arn_suffix
    TargetGroup  = var.website_lb_target_arn_suffix
  }
}