resource "aws_dynamodb_table" "comprehensive_recommendations" {
  name           = "ComprehensiveRecommendations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "FarmId"
  range_key      = "Timestamp"

  attribute {
    name = "FarmId"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "N"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  tags = {
    Name        = "ComprehensiveRecommendations"
    Environment = "Production"
  }
}