# Endpoint GET TASK PLAN
resource "aws_api_gateway_method_response" "get_task_plan_200" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.get_task_plan.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true 
  }
}

resource "aws_api_gateway_integration_response" "get_task_plan_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.get_task_plan.http_method
  status_code = aws_api_gateway_method_response.get_task_plan_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [
    aws_api_gateway_integration.lambda_task_plan
  ]
}

# OPTIONS METHOD
resource "aws_api_gateway_method" "options_method" {
  rest_api_id   = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id   = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.options_method.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options_200" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = "200"
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = aws_api_gateway_method_response.options_200.status_code
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
}