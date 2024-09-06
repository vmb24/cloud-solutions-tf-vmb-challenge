# Função auxiliar para configurar CORS
resource "aws_api_gateway_method" "options_method" {
  for_each = {
    "recommendations" = aws_api_gateway_resource.recommendations.id,
    "recommendations_by_topic" = aws_api_gateway_resource.recommendations_by_topic.id,
    "moisture" = aws_api_gateway_resource.moisture.id,
    "generate_recommendations" = aws_api_gateway_resource.generate_recommendations.id
  }

  rest_api_id   = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id   = each.value
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_integration" {
  for_each = aws_api_gateway_method.options_method

  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = jsonencode({
      statusCode = 200
    })
  }
}

resource "aws_api_gateway_method_response" "options_200" {
  for_each = aws_api_gateway_method.options_method

  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
  for_each = aws_api_gateway_method.options_method

  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = aws_api_gateway_method_response.options_200[each.key].status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_method_response.options_200]
}

# Adicionar respostas CORS para métodos existentes
resource "aws_api_gateway_method_response" "cors" {
  for_each = {
    "get_recommendations" = aws_api_gateway_method.get_recommendations,
    "get_recommendations_by_topic" = aws_api_gateway_method.get_recommendations_by_topic,
    "get_moisture" = aws_api_gateway_method.get_moisture,
    "post_generate_recommendations" = aws_api_gateway_method.post_generate_recommendations
  }

  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_integration_response" "cors_integration_response" {
  for_each = aws_api_gateway_method_response.cors

  rest_api_id = aws_api_gateway_rest_api.air_moisture_data_processing_recommendations_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = each.value.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.get_recommendations_integration,
    aws_api_gateway_integration.get_recommendations_by_topic_integration,
    aws_api_gateway_integration.get_moisture_integration,
    aws_api_gateway_integration.post_generate_recommendations_integration
  ]
}