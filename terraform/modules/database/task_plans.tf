# Tabela DynamoDB para Task Plans
resource "aws_dynamodb_table" "task_plans" {
  name           = "TaskPlans"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PlanId"
  range_key      = "CreatedAt"

  attribute {
    name = "PlanId"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "S"
  }

  attribute {
    name = "UserId"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "UserId"
    range_key          = "CreatedAt"
    projection_type    = "ALL"
  }
}