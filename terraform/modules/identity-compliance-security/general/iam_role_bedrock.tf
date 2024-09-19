# Processing Lambdas Bedrock Policies

resource "aws_iam_role_policy" "air_moisture_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.air_moisture_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "air_temperature_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.air_temperature_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "brightness_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.brightness_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_moisture_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.soil_moisture_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_temperature_data_processing_recommendations_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.soil_temperature_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

# Task Planner Lambdas Bedrock Policies

resource "aws_iam_role_policy" "air_moisture_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.air_moisture_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "air_temperature_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.air_temperature_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "brightness_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.brightness_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_moisture_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.soil_moisture_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_temperature_task_planner_bedrock_full_access" {
  name = "bedrock-full-access"
  role = var.soil_temperature_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:*"]
        Resource = "*"
      }
    ]
  })
}

# Specific Model Access Policies for Processing Lambdas

resource "aws_iam_role_policy" "air_moisture_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.air_moisture_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "air_temperature_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.air_temperature_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "brightness_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.brightness_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_moisture_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.soil_moisture_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_temperature_data_processing_recommendations_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.soil_temperature_data_processing_recommendations_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/ai21.j2-mid-v1",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/stability.stable-diffusion-xl-v1"
        ]
      }
    ]
  })
}

# Specific Model Access Policies for Task Planner Lambdas

resource "aws_iam_role_policy" "air_moisture_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.air_moisture_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1"
      }
    ]
  })
}

resource "aws_iam_role_policy" "air_temperature_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.air_temperature_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1"
      }
    ]
  })
}

resource "aws_iam_role_policy" "brightness_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.brightness_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_moisture_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.soil_moisture_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1"
      }
    ]
  })
}

resource "aws_iam_role_policy" "soil_temperature_task_planner_bedrock_specific_model_access" {
  name = "bedrock-specific-model-access"
  role = var.soil_temperature_task_planner_lambda_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-v2:1"
      }
    ]
  })
}