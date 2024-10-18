# DynamoDB Table
resource "aws_dynamodb_table" "users_accounts" {
  name           = "UsersAccounts"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }
}