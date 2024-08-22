# Tabela DynamoDB para Images
resource "aws_dynamodb_table" "images" {
  name           = "Images"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ImageId"

  attribute {
    name = "ImageId"
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