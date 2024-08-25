# Tabela MoistureHistory
resource "aws_dynamodb_table" "moisture_history" {
  name           = "MoistureHistory"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "DeviceId"
  range_key      = "Timestamp"

  attribute {
    name = "DeviceId"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "N"
  }

  global_secondary_index {
    name               = "TimestampIndex"
    hash_key           = "Timestamp"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "MoistureHistory"
    Environment = "production"
  }
}