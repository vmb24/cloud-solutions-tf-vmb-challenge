# API Gateway
resource "aws_api_gateway_rest_api" "air_temperature_task_planner_api" {
  name        = "AirTemperatureTaskPlannerAPI"
  description = "API for task planner application"
}

# Recursos da API Gateway
resource "aws_api_gateway_resource" "air_temperature_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  parent_id   = aws_api_gateway_rest_api.air_temperature_task_planner_api.root_resource_id
  path_part   = "task-plan"
}

resource "aws_api_gateway_resource" "generate_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  parent_id   = aws_api_gateway_rest_api.air_temperature_task_planner_api.root_resource_id
  path_part   = "generate-task-plan"
}

# Métodos da API Gateway
resource "aws_api_gateway_method" "get_task_plan" {
  rest_api_id   = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  resource_id   = aws_api_gateway_resource.air_temperature_task_plan.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integrações da API Gateway com Lambda
resource "aws_api_gateway_integration" "lambda_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.air_temperature_task_planner_api.id
  resource_id = aws_api_gateway_resource.air_temperature_task_plan.id
  http_method = aws_api_gateway_method.get_task_plan.http_method

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.air_temperature_task_planner.invoke_arn
}