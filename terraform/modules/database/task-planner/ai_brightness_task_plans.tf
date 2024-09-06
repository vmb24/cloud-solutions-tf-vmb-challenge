resource "aws_dynamodb_table" "ai_brightness_task_plans" {
  name           = "AIBrightnessTaskPlans"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "planId"
  range_key      = "createdAt"

  attribute {
    name = "planId"
    type = "S"
  }

  attribute {
    name = "createdAt"
    type = "S"
  }

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "averageBrightness"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "userId"
    range_key          = "createdAt"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "BrightnessIndex"
    hash_key           = "planId"
    range_key          = "averageBrightness"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "status"
    range_key          = "createdAt"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "AIBrightnessTaskPlans"
    Environment = "production"
  }
}