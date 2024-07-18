resource "aws_dynamodb_table" "weather_data" {
  name           = "WeatherData"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "WeatherID"
  range_key      = "FarmerID"

  attribute {
    name = "WeatherID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "WeatherData"
  }
}
