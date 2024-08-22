output "moisture_iot_rule_arn" {
  value = aws_iot_topic_rule.moisture_iot_rule.arn
}

# Output para o ARN do tópico SNS
output "sns_topic_arn" {
  value = aws_sns_topic.iot_topic.arn
}