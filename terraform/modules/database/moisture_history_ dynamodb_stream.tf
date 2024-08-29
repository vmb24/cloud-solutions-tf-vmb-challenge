resource "aws_lambda_event_source_mapping" "dynamodb_stream" {
  event_source_arn  = aws_dynamodb_table.moisture_history.stream_arn
  function_name     = var.moisture_task_planner_lambda_arn
  starting_position = "LATEST"
}