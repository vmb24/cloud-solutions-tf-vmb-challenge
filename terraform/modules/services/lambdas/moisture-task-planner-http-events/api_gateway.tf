# API Gateway
resource "aws_api_gateway_rest_api" "moisture_task_planner_http_events_api" {
  name        = "MoistureTaskPlannerHttpEventsAPI"
  description = "API for task planner http events application"
}

# Recursos da API Gateway
resource "aws_api_gateway_resource" "moisture_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  parent_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.root_resource_id
  path_part   = "task-plan-http-events"
}

resource "aws_api_gateway_resource" "images" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  parent_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.root_resource_id
  path_part   = "images"
}

resource "aws_api_gateway_resource" "videos" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  parent_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.root_resource_id
  path_part   = "videos"
}

resource "aws_api_gateway_resource" "generate_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  parent_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.root_resource_id
  path_part   = "generate-task-plan-http-events"
}

# Métodos da API Gateway
resource "aws_api_gateway_method" "get_task_plan" {
  rest_api_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id   = aws_api_gateway_resource.moisture_task_plan.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_images" {
  rest_api_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_videos" {
  rest_api_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id   = aws_api_gateway_resource.videos.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_generate_task_plan" {
  rest_api_id   = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id   = aws_api_gateway_resource.generate_task_plan.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integrações da API Gateway com Lambda
resource "aws_api_gateway_integration" "lambda_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id = aws_api_gateway_resource.moisture_task_plan.id
  http_method = aws_api_gateway_method.get_task_plan.http_method

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.moisture_task_planner_http_events.invoke_arn
}

resource "aws_api_gateway_integration" "lambda_images" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id = aws_api_gateway_resource.images.id
  http_method = aws_api_gateway_method.get_images.http_method

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.moisture_task_planner_http_events.invoke_arn
}

resource "aws_api_gateway_integration" "lambda_videos" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id = aws_api_gateway_resource.videos.id
  http_method = aws_api_gateway_method.get_videos.http_method

  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.moisture_task_planner_http_events.invoke_arn
}

resource "aws_api_gateway_integration" "lambda_generate_task_plan" {
  rest_api_id = aws_api_gateway_rest_api.moisture_task_planner_http_events_api.id
  resource_id = aws_api_gateway_resource.generate_task_plan.id
  http_method = aws_api_gateway_method.post_generate_task_plan.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.moisture_task_planner_http_events.invoke_arn
}