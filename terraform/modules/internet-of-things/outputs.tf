# Certificates
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

# Topic ARNS
output "air_moisture_iot_rule_arn" {
  value = aws_iot_topic_rule.air_moisture_rule.arn
}

output "air_temperature_iot_rule_arn" {
  value = aws_iot_topic_rule.air_temperature_rule.arn
}

output "brightness_iot_rule_arn" {
  value = aws_iot_topic_rule.brightness_rule.arn
}

output "soil_moisture_iot_rule_arn" {
  value = aws_iot_topic_rule.soil_moisture_rule.arn
}

output "soil_temperature_iot_rule_arn" {
  value = aws_iot_topic_rule.soil_temperature_rule.arn
}