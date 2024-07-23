resource "aws_api_gateway_rest_api" "greenhouse_microservice" {
  name        = "greenhouse-microservice"
  description = "Greenhouse Service API Gateway"
}

resource "aws_api_gateway_resource" "greenhouse_service" {
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  parent_id   = aws_api_gateway_rest_api.greenhouse_microservice.root_resource_id
  path_part   = "greenhouse-service"
}

# POST Method
resource "aws_api_gateway_method" "post_greenhouse_service" {
  rest_api_id   = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id   = aws_api_gateway_resource.greenhouse_service.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_greenhouse_service" {
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id = aws_api_gateway_resource.greenhouse_service.id
  http_method = aws_api_gateway_method.post_greenhouse_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/greenhouse-service"
  integration_http_method = "POST"
}

# GET Method
resource "aws_api_gateway_method" "get_greenhouse_service" {
  rest_api_id   = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id   = aws_api_gateway_resource.greenhouse_service.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_greenhouse_service" {
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id = aws_api_gateway_resource.greenhouse_service.id
  http_method = aws_api_gateway_method.get_greenhouse_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/greenhouse-service"
  integration_http_method = "GET"
}

# PUT Method
resource "aws_api_gateway_method" "put_greenhouse_service" {
  rest_api_id   = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id   = aws_api_gateway_resource.greenhouse_service.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "put_greenhouse_service" {
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id = aws_api_gateway_resource.greenhouse_service.id
  http_method = aws_api_gateway_method.put_greenhouse_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/greenhouse-service"
  integration_http_method = "PUT"
}

# DELETE Method
resource "aws_api_gateway_method" "delete_greenhouse_service" {
  rest_api_id   = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id   = aws_api_gateway_resource.greenhouse_service.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_greenhouse_service" {
  rest_api_id = aws_api_gateway_rest_api.greenhouse_microservice.id
  resource_id = aws_api_gateway_resource.greenhouse_service.id
  http_method = aws_api_gateway_method.delete_greenhouse_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/greenhouse-service"
  integration_http_method = "DELETE"
}
