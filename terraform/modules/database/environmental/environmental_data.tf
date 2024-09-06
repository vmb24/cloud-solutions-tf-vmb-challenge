resource "aws_dynamodb_table" "environmental_data" {
  name           = "EnvironmentalData"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "SensorId"
  range_key      = "Timestamp"

  attribute {
    name = "SensorId"
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
    Name        = "EnvironmentalData"
    Environment = "Production"
  }
}