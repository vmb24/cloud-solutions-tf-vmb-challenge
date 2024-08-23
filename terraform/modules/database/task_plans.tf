# Tabela DynamoDB para Task Plans (modificada)
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

  attribute {
    name = "TaskPlan"
    type = "S"
  }

  attribute {
    name = "AverageMoisture"
    type = "N"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "UserId"
    range_key          = "CreatedAt"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "TaskPlanIndex"
    hash_key           = "TaskPlan"
    range_key          = "CreatedAt"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "MoistureIndex"
    hash_key           = "PlanId"
    range_key          = "AverageMoisture"
    projection_type    = "ALL"
  }
}