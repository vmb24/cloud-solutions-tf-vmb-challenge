resource "aws_dynamodb_table" "soil_metrics" {
  name           = "SoilMetrics"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "MetricID"
  range_key      = "FarmerID"

  attribute {
    name = "MetricID"
    type = "S"
  }

  attribute {
    name = "FarmerID"
    type = "S"
  }

  tags = {
    Name = "SoilMetrics"
  }
}
