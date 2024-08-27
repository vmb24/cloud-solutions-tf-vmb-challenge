# Criação do tópico SNS
resource "aws_sns_topic" "iot_topic" {
  name = "iot_sns_notifications"
}