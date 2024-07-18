resource "aws_dynamodb_table" "image_analysis_results" {
  name           = "ImageAnalysisResults"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "AnalysisID"

  attribute {
    name = "AnalysisID"
    type = "S"
  }

  tags = {
    Name = "ImageAnalysisResults"
  }
}
