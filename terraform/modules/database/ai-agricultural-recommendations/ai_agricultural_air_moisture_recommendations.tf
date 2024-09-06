resource "aws_dynamodb_table" "ai_agricultural_air_moisture_recommendations" {
  name           = "AIAgriculturalAirMoistureRecommendations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "date"

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "thing_name"
    type = "S"
  }

  attribute {
    name = "last_update"
    type = "S"
  }

  global_secondary_index {
    name               = "ThingNameIndex"
    hash_key           = "thing_name"
    range_key          = "last_update"
    projection_type    = "ALL"
  }

  tags = {
    Environment = "production"
    Project     = "AgricultureOptimization"
  }
}