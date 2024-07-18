resource "aws_dynamodb_table" "crop_health" {
  name           = "CropHealth"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "CropID"
  range_key      = "FarmerID"

  attribute {
    name = "CropID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "CropHealth"
  }
}
