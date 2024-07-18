resource "aws_dynamodb_table" "equipment_health" {
  name           = "EquipmentHealth"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "EquipmentID"
  range_key      = "FarmerID"

  attribute {
    name = "EquipmentID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "EquipmentHealth"
  }
}
