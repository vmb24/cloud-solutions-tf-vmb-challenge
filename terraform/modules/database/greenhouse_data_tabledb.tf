resource "aws_dynamodb_table" "greenhouse_data" {
  name           = "GreenhouseData"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "GreenhouseID"
  range_key      = "FarmerID"

  attribute {
    name = "GreenhouseID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "GreenhouseData"
  }
}
