# Criação do API Gateway REST API
resource "aws_api_gateway_rest_api" "air_moisture_data_processing_recommendations_api" {
  name        = "AirMoistureRecommendationsAPI"
  description = "API for Recommendations in Precision Agriculture"
}

# Recurso /recommendations
resource "aws_api_gateway_resource" "recommendations" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  parent_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.root_resource_id
  path_part   = "recommendations"
}

# Método GET para /recommendations
resource "aws_api_gateway_method" "get_recommendations" {
  rest_api_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id   = aws_api_gateway_resource.recommendations.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integração do método GET /recommendations com a função Lambda
resource "aws_api_gateway_integration" "get_recommendations_integration" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = aws_api_gateway_resource.recommendations.id
  http_method = aws_api_gateway_method.get_recommendations.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.air_moisture_data_processing_recommendations.invoke_arn
}

# Recurso /recommendations/by-topic
resource "aws_api_gateway_resource" "recommendations_by_topic" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  parent_id   = aws_api_gateway_resource.recommendations.id
  path_part   = "by-topic"
}

# Método GET para /recommendations/by-topic
resource "aws_api_gateway_method" "get_recommendations_by_topic" {
  rest_api_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id   = aws_api_gateway_resource.recommendations_by_topic.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.querystring.topic" = true
  }
}

# Integração do método GET /recommendations/by-topic com a função Lambda
resource "aws_api_gateway_integration" "get_recommendations_by_topic_integration" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = aws_api_gateway_resource.recommendations_by_topic.id
  http_method = aws_api_gateway_method.get_recommendations_by_topic.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.air_moisture_data_processing_recommendations.invoke_arn
}

# Recurso /moisture
resource "aws_api_gateway_resource" "moisture" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  parent_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.root_resource_id
  path_part   = "moisture"
}

# Método GET para /moisture
resource "aws_api_gateway_method" "get_moisture" {
  rest_api_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id   = aws_api_gateway_resource.moisture.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integração do método GET /moisture com a função Lambda
resource "aws_api_gateway_integration" "get_moisture_integration" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = aws_api_gateway_resource.moisture.id
  http_method = aws_api_gateway_method.get_moisture.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.air_moisture_data_processing_recommendations.invoke_arn
}

# Recurso /generate-recommendations
resource "aws_api_gateway_resource" "generate_recommendations" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  parent_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.root_resource_id
  path_part   = "generate-recommendations"
}

# Método POST para /generate-recommendations
resource "aws_api_gateway_method" "post_generate_recommendations" {
  rest_api_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id   = aws_api_gateway_resource.generate_recommendations.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integração do método POST /generate-recommendations com a função Lambda
resource "aws_api_gateway_integration" "post_generate_recommendations_integration" {
  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = aws_api_gateway_resource.generate_recommendations.id
  http_method = aws_api_gateway_method.post_generate_recommendations.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.air_moisture_data_processing_recommendations.invoke_arn
}