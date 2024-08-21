# Trigger do DynamoDB Streams
resource "aws_lambda_event_source_mapping" "dynamodb_stream" {
  event_source_arn  = "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/AverageMoisture/stream/STREAM_ID"
  function_name     = aws_lambda_function.moisture_task_planner.arn
  starting_position = "LATEST"
}