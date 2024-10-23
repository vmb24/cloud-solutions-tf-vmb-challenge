# Policy template for Bedrock full access
resource "aws_iam_role_policy" "bedrock_full_access" {
  for_each = {
    air_moisture_data_processing_recommendations   = var.air_moisture_data_processing_recommendations_lambda_role_id
    air_temperature_data_processing_recommendations = var.air_temperature_data_processing_recommendations_lambda_role_id
    brightness_data_processing_recommendations     = var.brightness_data_processing_recommendations_lambda_role_id
    soil_moisture_data_processing_recommendations  = var.soil_moisture_data_processing_recommendations_lambda_role_id
    soil_temperature_data_processing_recommendations = var.soil_temperature_data_processing_recommendations_lambda_role_id
    air_moisture_task_planner                      = var.air_moisture_task_planner_lambda_role_id
    air_temperature_task_planner                   = var.air_temperature_task_planner_lambda_role_id
    brightness_task_planner                        = var.brightness_task_planner_lambda_role_id
    soil_moisture_task_planner                     = var.soil_moisture_task_planner_lambda_role_id
    soil_temperature_task_planner                  = var.soil_temperature_task_planner_lambda_role_id
  }

  name = "${each.key}-bedrock-full-access"
  role = each.value

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
        ]
      }
    ]
  })
}
