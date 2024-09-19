# Função auxiliar para configurar CORS
resource "aws_api_gateway_method" "air_temperature_options_method" {
  for_each = {
    "air_temperature_task_plan" = aws_api_gateway_resource.air_temperature_task_plan.id,
    "generate_task_plan" = aws_api_gateway_resource.generate_task_plan.id
  }

  rest_api_id   = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  resource_id   = each.value
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_integration" {
  for_each = aws_api_gateway_method.air_temperature_options_method

  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
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
  for_each = aws_api_gateway_method.air_temperature_options_method

  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
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
  for_each = aws_api_gateway_method.air_temperature_options_method

  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
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
    "get_task_plan" = aws_api_gateway_method.get_task_plan,
  }

  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_integration_response" "cors_integration_response" {
  for_each = aws_api_gateway_method_response.cors

  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = each.value.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.lambda_task_plan,
  ]
}