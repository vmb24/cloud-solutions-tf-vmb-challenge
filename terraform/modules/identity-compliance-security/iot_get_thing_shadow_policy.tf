# Resgatando o valor do account id dinamicamente
data "aws_caller_identity" "current" {}

# Criar a política IAM
resource "aws_iam_policy" "iot_get_thing_shadow_policy" {
  name        = "IoTGetThingShadowPolicy"
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
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:thing/parking_sensor"
      }
    ]
  })
}

# Anexar a política à role da função Lambda
resource "aws_iam_role_policy_attachment" "parking_spot_status_update_lambda_iot_policy_attachment" {
  role       = aws_iam_role.parking_spot_status_update_lambda_role.name
  policy_arn = aws_iam_policy.iot_get_thing_shadow_policy.arn
}