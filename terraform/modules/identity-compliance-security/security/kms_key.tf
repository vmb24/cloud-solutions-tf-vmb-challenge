resource "aws_kms_key" "app_key" {
  description = "KMS key for agricultural application"
  enable_key_rotation = true
}

resource "aws_kms_alias" "app_key_alias" {
  name          = "alias/agricultural-app-key"
  target_key_id = aws_kms_key.app_key.key_id
}