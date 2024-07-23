resource "aws_api_gateway_rest_api" "weather_microservice" {
  name        = "weather-microservice"
  description = "Weather Service API Gateway"
}

resource "aws_api_gateway_resource" "weather_service" {
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  parent_id   = aws_api_gateway_rest_api.weather_microservice.root_resource_id
  path_part   = "weather-service"
}

# POST Method
resource "aws_api_gateway_method" "post_weather_service" {
  rest_api_id   = aws_api_gateway_rest_api.weather_microservice.id
  resource_id   = aws_api_gateway_resource.weather_service.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_weather_service" {
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  resource_id = aws_api_gateway_resource.weather_service.id
  http_method = aws_api_gateway_method.post_weather_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/weather-service"
  integration_http_method = "POST"
}

# GET Method
resource "aws_api_gateway_method" "get_weather_service" {
  rest_api_id   = aws_api_gateway_rest_api.weather_microservice.id
  resource_id   = aws_api_gateway_resource.weather_service.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_weather_service" {
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  resource_id = aws_api_gateway_resource.weather_service.id
  http_method = aws_api_gateway_method.get_weather_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/weather-service"
  integration_http_method = "GET"
}

# PUT Method
resource "aws_api_gateway_method" "put_weather_service" {
  rest_api_id   = aws_api_gateway_rest_api.weather_microservice.id
  resource_id   = aws_api_gateway_resource.weather_service.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "put_weather_service" {
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  resource_id = aws_api_gateway_resource.weather_service.id
  http_method = aws_api_gateway_method.put_weather_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/weather-service"
  integration_http_method = "PUT"
}

# DELETE Method
resource "aws_api_gateway_method" "delete_weather_service" {
  rest_api_id   = aws_api_gateway_rest_api.weather_microservice.id
  resource_id   = aws_api_gateway_resource.weather_service.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_weather_service" {
  rest_api_id = aws_api_gateway_rest_api.weather_microservice.id
  resource_id = aws_api_gateway_resource.weather_service.id
  http_method = aws_api_gateway_method.delete_weather_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/weather-service"
  integration_http_method = "DELETE"
}
