resource "aws_dynamodb_table" "brightness_history" {
  name           = "BrightnessHistory"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "status"
  range_key      = "timestamp"

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "brightness"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "planGenerated"
    type = "S"
  }

  global_secondary_index {
    name               = "DateTimestampIndex"
    hash_key           = "date"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "BrightnessTimestampIndex"
    hash_key           = "brightness"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "PlanGeneratedIndex"
    hash_key           = "planGenerated"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  tags = {
    Name        = "BrightnessHistory"
    Environment = "production"
  }
}