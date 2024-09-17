# Agricultural Reccomendations Tables
output "ai_agricultural_air_moisture_recommendations_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_agricultural_air_moisture_recommendations.arn
}

output "ai_agricultural_air_temperature_recommendations_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_agricultural_air_temperature_recommendations.arn
}

output "ai_agricultural_brightness_recommendations_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_agricultural_brightness_recommendations.arn
}

output "ai_agricultural_soil_moisture_recommendations_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_agricultural_soil_moisture_recommendations.arn
}

output "ai_agricultural_soil_temperature_recommendations_dynamodb_table_arn" {
  value = aws_dynamodb_table.ai_agricultural_soil_temperature_recommendations.arn
}
