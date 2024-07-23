resource "aws_lambda_function" "llm_weather_recommendations" {
  function_name = "llm-weather-recommendations-lambda"
  role          = var.iam_role_lambda_exec_arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.llm_weather_recommendations.repository_url}:latest"
  timeout       = 300

  environment {
    variables = {
      TABLE_NAME = "WeatherRecommendations"
    }
  }

  lifecycle {
    ignore_changes = [image_uri]  # Ignora mudanças no URI da imagem para evitar recriação
  }
}
