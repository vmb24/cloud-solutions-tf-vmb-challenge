# Generate images lambdas ARN
output "generate_images_to_air_moisture_metric_lambda_role_arn" {
  value = aws_iam_role.generate_images_to_air_moisture_metric_lambda_role.arn
}

output "generate_images_air_temperature_metric_lambda_role_arn" {
  value = aws_iam_role.generate_images_to_air_temperature_metric_lambda_role.arn
}

output "generate_images_brightness_metric_lambda_role_arn" {
  value = aws_iam_role.generate_images_to_brightness_metric_lambda_role.arn
}

output "generate_images_soil_moisture_metric_lambda_role_arn" {
  value = aws_iam_role.generate_images_to_soil_moisture_metric_lambda_role.arn
}

output "generate_images_soil_temperature_metric_lambda_role_arn" {
  value = aws_iam_role.generate_images_to_soil_temperature_metric_lambda_role.arn
}