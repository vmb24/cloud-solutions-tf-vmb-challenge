# History Tables
output "air_moisture_history_dynamodb_table_arn" {
  value = aws_dynamodb_table.air_moisture_history.arn
}

output "air_temperature_history_dynamodb_table_arn" {
  value = aws_dynamodb_table.air_temperature_history.arn
}

output "brightness_history_dynamodb_table_arn" {
  value = aws_dynamodb_table.brightness_history.arn
}

output "soil_moisture_history_dynamodb_table_arn" {
  value = aws_dynamodb_table.soil_moisture_history.arn
}

output "soil_temperature_history_dynamodb_table_arn" {
  value = aws_dynamodb_table.soil_temperature_history.arn
}