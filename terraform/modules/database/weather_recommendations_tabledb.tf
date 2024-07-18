resource "aws_dynamodb_table" "weather_recommendations" {
  name           = "WeatherRecommendations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "RecommendationID"
  range_key      = "FarmerID"

  attribute {
    name = "RecommendationID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "WeatherRecommendations"
  }
}
