# Configuração do AWS Config Recorder
resource "aws_config_configuration_recorder" "app_recorder" {
  name     = "agricultural-app-recorder"
  role_arn = aws_iam_role.config_role.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

# Configuração do AWS Config Delivery Channel
resource "aws_config_delivery_channel" "app_channel" {
  name           = "agricultural-app-channel"
  s3_bucket_name = aws_s3_bucket.config_bucket.id
  depends_on     = [aws_config_configuration_recorder.app_recorder]
}

# Habilitar o AWS Config Recorder
resource "aws_config_configuration_recorder_status" "app_recorder_status" {
  name       = aws_config_configuration_recorder.app_recorder.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.app_channel]
}