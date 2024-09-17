resource "aws_dynamodb_table" "agrix_feedback" {
  name           = "AgrixFeedback"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"
  range_key      = "feedbackId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "feedbackId"
    type = "S"
  }
}