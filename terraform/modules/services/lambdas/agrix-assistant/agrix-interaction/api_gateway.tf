# Criação do API Gateway
resource "aws_api_gateway_rest_api" "agrix_api" {
  name        = "agrix-assistant-api"
  description = "API for Agrix Assistant"
}

# Recurso para recomendações
resource "aws_api_gateway_resource" "recommendations" {
  rest_api_id = aws_api_gateway_rest_api.agrix_api.id
  parent_id   = aws_api_gateway_rest_api.agrix_api.root_resource_id
  path_part   = "recommendations"
}

# Método GET para recomendações
resource "aws_api_gateway_method" "get_recommendations" {
  rest_api_id   = aws_api_gateway_rest_api.agrix_api.id
  resource_id   = aws_api_gateway_resource.recommendations.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integração do método GET com Lambda
resource "aws_api_gateway_integration" "get_recommendations_integration" {
  rest_api_id = aws_api_gateway_rest_api.agrix_api.id
  resource_id = aws_api_gateway_resource.recommendations.id
  http_method = aws_api_gateway_method.get_recommendations.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.agrix_interaction_handler.invoke_arn
}

# Recurso para interações
resource "aws_api_gateway_resource" "interact" {
  rest_api_id = aws_api_gateway_rest_api.agrix_api.id
  parent_id   = aws_api_gateway_rest_api.agrix_api.root_resource_id
  path_part   = "interact"
}

# Método POST para interações
resource "aws_api_gateway_method" "post_interact" {
  rest_api_id   = aws_api_gateway_rest_api.agrix_api.id
  resource_id   = aws_api_gateway_resource.interact.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integração do método POST com Lambda
resource "aws_api_gateway_integration" "post_interact_integration" {
  rest_api_id = aws_api_gateway_rest_api.agrix_api.id
  resource_id = aws_api_gateway_resource.interact.id
  http_method = aws_api_gateway_method.post_interact.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.agrix_interaction_handler.invoke_arn
}

# Implantação do API Gateway
resource "aws_api_gateway_deployment" "agrix_deployment" {
  depends_on = [
    aws_api_gateway_integration.get_recommendations_integration,
    aws_api_gateway_integration.post_interact_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.agrix_api.id
  stage_name  = "prod"
}
