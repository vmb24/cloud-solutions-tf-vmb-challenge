# DynamoDB Tables
resource "aws_dynamodb_table" "soil_moisture_media_metadata" {
  name           = "SoilMoistureMedia"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "media_id"
  range_key      = "timestamp"

  attribute {
    name = "media_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  ttl {
    attribute_name = "expiration_time"
    enabled        = true
  }

  tags = {
    Name        = "SoilMoistureMedia"
    Environment = "Production"
  }
}