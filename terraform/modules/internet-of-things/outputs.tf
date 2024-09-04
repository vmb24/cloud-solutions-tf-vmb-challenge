output "moisture_iot_rule_arn" {
  value = aws_iot_topic_rule.moisture_iot_rule.arn
}

# Output para o ARN do tópico SNS
output "sns_topic_arn" {
  value = aws_sns_topic.iot_topic.arn
}

output "certificate_pem" {
  value = aws_iot_certificate.iot_cert.certificate_pem
  sensitive = true
}

output "public_key" {
  value = aws_iot_certificate.iot_cert.public_key
  sensitive = true
}

output "private_key" {
  value = aws_iot_certificate.iot_cert.private_key
  sensitive = true
}

output "iot_endpoint" {
  value = data.aws_iot_endpoint.endpoint.endpoint_address
}