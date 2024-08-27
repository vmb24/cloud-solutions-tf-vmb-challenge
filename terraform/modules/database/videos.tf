# Tabela DynamoDB para Videos
resource "aws_dynamodb_table" "videos" {
  name           = "Videos"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "VideoId"

  attribute {
    name = "VideoId"
    type = "S"
  }

  attribute {
    name = "UserId"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "UserId"
    projection_type    = "ALL"
  }
}