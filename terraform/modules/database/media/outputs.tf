# Media ARN Tables
output "air_moisture_media_media_dynamodb_table_arn" {
  value = aws_dynamodb_table.air_moisture_media_metadata.arn
}

output "air_temperature_media_media_dynamodb_table_arn" {
  value = aws_dynamodb_table.air_temperature_media_metadata.arn
}

output "brightness_media_media_dynamodb_table_arn" {
  value = aws_dynamodb_table.brightness_media_metadata.arn
}

output "soil_moisture_media_media_dynamodb_table_arn" {
  value = aws_dynamodb_table.soil_moisture_media_metadata.arn
}

output "soil_temperature_media_media_dynamodb_table_arn" {
  value = aws_dynamodb_table.soil_temperature_media_metadata.arn
}