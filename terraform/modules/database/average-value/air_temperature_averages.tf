# Tabela TemperatureAverages
resource "aws_dynamodb_table" "air_temperature_averages" {
  name           = "AirTemperatureAverages"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "date"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "thing_name"
    type = "S"
  }

  global_secondary_index {
    name               = "ThingNameIndex"
    hash_key           = "thing_name"
    range_key          = "date"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "AirTemperatureAverages"
    Environment = "production"
  }
}