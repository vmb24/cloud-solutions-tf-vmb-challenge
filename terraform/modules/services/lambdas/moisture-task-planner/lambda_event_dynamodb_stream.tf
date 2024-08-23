# Trigger do DynamoDB Streams
resource "aws_lambda_event_source_mapping" "dynamodb_stream" {
  event_source_arn  = var.agricultural_moisture_recommendations_tabledb_stream_arn
  function_name     = aws_lambda_function.moisture_task_planner.arn
  starting_position = "LATEST"
}