# API Gateway
resource "aws_api_gateway_rest_api" "soil_temperature_task_planner_api" {
  name        = "SoiTemperatureTaskPlannerAPI"
  description = "API for task planner application"
}

# Recursos da API Gateway
resource "aws_api_gateway_resource" "soil_temperature_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  parent_id   = aws_api_gateway_rest_api.soil_temperature_task_planner_api.root_resource_id
  path_part   = "task-plan"
}

# Métodos da API Gateway - Get Task Plan
resource "aws_api_gateway_method" "get_task_plan" {
  rest_api_id   = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id   = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.soil_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.soil_temperature_task_plan.id
  http_method = aws_api_gateway_method.get_task_plan.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.soil_temperature_task_planner.invoke_arn
}