# Tabela MoistureAverages
resource "aws_dynamodb_table" "moisture_averages" {
  name           = "MoistureAverages"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "DeviceId"
  range_key      = "Date"

  attribute {
    name = "DeviceId"
    type = "S"
  }

  attribute {
    name = "Date"
    type = "S"
  }

  global_secondary_index {
    name               = "DateIndex"
    hash_key           = "Date"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "MoistureAverages"
    Environment = "production"
  }
}