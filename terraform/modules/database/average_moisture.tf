# Tabela DynamoDB para AverageMoisture
resource "aws_dynamodb_table" "average_moisture" {
  name           = "AverageMoisture"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "SensorId"
  range_key      = "Timestamp"

  attribute {
    name = "SensorId"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "S"
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}