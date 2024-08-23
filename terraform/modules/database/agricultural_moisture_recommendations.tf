resource "aws_dynamodb_table" "agricultural_moisture_recommendations" {
  name           = "AgriculturalRecommendations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "timestamp"
  range_key      = "thing_name"

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "thing_name"
    type = "S"
  }

  attribute {
    name = "topic"
    type = "S"
  }

  # Atributos adicionais
  attribute {
    name = "recommendation"
    type = "S"
  }

  attribute {
    name = "moisture"
    type = "N"
  }

  attribute {
    name = "status"
    type = "S"
  }

  global_secondary_index {
    name               = "TopicIndex"
    hash_key           = "topic"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "RecommendationIndex"
    hash_key           = "recommendation"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "MoistureIndex"
    hash_key           = "moisture"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "status"
    projection_type    = "ALL"
  }

  tags = {
    Environment = "production"
    Project     = "AgricultureOptimization"
  }
}