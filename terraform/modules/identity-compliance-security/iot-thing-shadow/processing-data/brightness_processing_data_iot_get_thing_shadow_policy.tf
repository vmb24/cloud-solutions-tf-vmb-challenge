# Resgatando o valor do account id dinamicamente
data "aws_caller_identity" "brightness_processing_data_current_caller_identity" {}

# Criar a política IAM
resource "aws_iam_policy" "brightness_processing_data_iot_get_thing_shadow_policy" {
  name        = "BrightnessProcessingIoTGetThingShadowPolicy"
  path        = "/"
  description = "Permite a ação GetThingShadow no IoT Core"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iot:GetThingShadow"
        ]
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.brightness_processing_data_current_caller_identity.account_id}:thing/brightness_sensor"
      }
    ]
  })
}

# Anexar a política à role da função Lambda
resource "aws_iam_role_policy_attachment" "brightness_task_planner_lambda_iot_policy_attachment" {
  role       = var.brightness_data_processing_recommendations_lambda_role_name
  policy_arn = aws_iam_policy.brightness_processing_data_iot_get_thing_shadow_policy.arn
}