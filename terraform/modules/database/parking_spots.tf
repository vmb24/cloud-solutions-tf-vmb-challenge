resource "aws_dynamodb_table" "parking_spots" {
  name           = "ParkingSpots"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "spot_id"

  attribute {
    name = "spot_id"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "status"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "parking-spots-table"
    Environment = "production"
  }
}