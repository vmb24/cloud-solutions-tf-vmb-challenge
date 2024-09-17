resource "aws_lex_bot" "agrix_bot" {
  name                     = "AgrixAssistant"
  description              = "Virtual assistant for Agrix platform"
  idle_session_ttl_in_seconds = 300
  voice_id                 = "Joanna"
  process_behavior         = "BUILD"
  child_directed           = false

  abort_statement {
    message {
      content      = "Sorry, I'm not able to assist at this time. Please try again later."
      content_type = "PlainText"
    }
  }

  clarification_prompt {
    max_attempts = 2
    message {
      content      = "I didn't understand. Can you please rephrase?"
      content_type = "PlainText"
    }
  }

  intent {
    intent_name    = "GetSoilMoistureRecommendation"
    intent_version = "$LATEST"
  }

  intent {
    intent_name    = "GetSoilTemperatureRecommendation"
    intent_version = "$LATEST"
  }

  intent {
    intent_name    = "GetAirMoistureRecommendation"
    intent_version = "$LATEST"
  }

  intent {
    intent_name    = "GetAirTemperatureRecommendation"
    intent_version = "$LATEST"
  }

  intent {
    intent_name    = "GetBrightnessRecommendation"
    intent_version = "$LATEST"
  }
}

resource "aws_lex_intent" "get_soil_moisture_recommendation" {
  name = "GetSoilMoistureRecommendation"
  
  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = aws_lambda_function.soil_moisture_fulfillment.arn
    }
  }

  sample_utterances = [
    "What's the soil moisture recommendation?",
    "Tell me about soil moisture",
    "Do I need to water my plants?"
  ]
}

# Defina intents similares para as outras métricas

resource "aws_lambda_function" "soil_moisture_fulfillment" {
  filename      = "soil_moisture_fulfillment.zip"
  function_name = "soil_moisture_fulfillment"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      PROCESSING_LAMBDA_ARN = aws_lambda_function.processing_moisture_recommendations.arn
      TASK_PLANNER_LAMBDA_ARN = aws_lambda_function.moisture_task_planner.arn
    }
  }
}

# Defina Lambdas de fulfillment similares para as outras métricas