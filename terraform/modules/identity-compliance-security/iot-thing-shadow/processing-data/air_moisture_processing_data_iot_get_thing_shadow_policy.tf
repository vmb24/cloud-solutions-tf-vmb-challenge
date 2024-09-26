# Resgatando o valor do account id dinamicamente
data "aws_caller_identity" "air_moisture_processing_data_current_caller_identity" {}

# Criar a política IAM
resource "aws_iam_policy" "air_moisture_processing_data_iot_get_thing_shadow_policy" {
  name        = "AirMoistureProcessingIoTGetThingShadowPolicy"
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
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.air_moisture_processing_data_current_caller_identity.account_id}:thing/air_moisture_sensor"
      }
    ]
  })
}

# Anexar a política à role da função Lambda
resource "aws_iam_role_policy_attachment" "air_moisture_task_planner_lambda_iot_policy_attachment" {
  role       = var.air_moisture_data_processing_recommendations_lambda_role_name
  policy_arn = aws_iam_policy.air_moisture_processing_data_iot_get_thing_shadow_policy.arn
}