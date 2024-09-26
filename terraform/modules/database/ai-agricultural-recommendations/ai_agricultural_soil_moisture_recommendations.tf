resource "aws_dynamodb_table" "ai_agricultural_soil_moisture_recommendations" {
  name           = "AIAgriculturalSoilMoistureRecommendations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "date"

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "topic_name"
    type = "S"
  }

  attribute {
    name = "last_update"
    type = "S"
  }

  global_secondary_index {
    name               = "ThingNameIndex"
    hash_key           = "topic_name"
    range_key          = "last_update"
    projection_type    = "ALL"
  }

  tags = {
    Environment = "production"
    Project     = "AgricultureOptimization"
  }
}