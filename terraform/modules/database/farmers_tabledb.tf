resource "aws_dynamodb_table" "farmers" {
  name           = "Farmers"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "FarmerID"

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "Farmers"
  }
}
