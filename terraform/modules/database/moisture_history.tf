# Tabela MoistureHistory
resource "aws_dynamodb_table" "moisture_history" {
  name           = "MoistureHistory"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "date"
  range_key      = "timestamp"

  attribute {
    name = "timestamp"
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
    name               = "ThingNameIndex"
    hash_key           = "thing_name"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "status"
    range_key          = "timestamp"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "MoistureIndex"
    hash_key           = "date"
    range_key          = "moisture"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "MoistureHistory"
    Environment = "production"
  }
}