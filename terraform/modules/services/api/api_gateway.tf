resource "aws_api_gateway_rest_api" "tech4parking_api" {
  name        = "farmer-microservice"
  description = "Farmer Service API Gateway"
}

resource "aws_api_gateway_resource" "farmer_service" {
  rest_api_id = aws_api_gateway_rest_api.tech4parking_api.id
  parent_id   = aws_api_gateway_rest_api.tech4parking_api.root_resource_id
  path_part   = "farmer-service"
}

# POST Method
resource "aws_api_gateway_method" "post_farmer_service" {
  rest_api_id   = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id   = aws_api_gateway_resource.farmer_service.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_farmer_service" {
  rest_api_id = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id = aws_api_gateway_resource.farmer_service.id
  http_method = aws_api_gateway_method.post_farmer_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/farmer-service"
  integration_http_method = "POST"
}

# GET Method
resource "aws_api_gateway_method" "get_farmer_service" {
  rest_api_id   = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id   = aws_api_gateway_resource.farmer_service.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_farmer_service" {
  rest_api_id = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id = aws_api_gateway_resource.farmer_service.id
  http_method = aws_api_gateway_method.get_farmer_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/farmer-service"
  integration_http_method = "GET"
}

# PUT Method
resource "aws_api_gateway_method" "put_farmer_service" {
  rest_api_id   = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id   = aws_api_gateway_resource.farmer_service.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "put_farmer_service" {
  rest_api_id = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id = aws_api_gateway_resource.farmer_service.id
  http_method = aws_api_gateway_method.put_farmer_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/farmer-service"
  integration_http_method = "PUT"
}

# DELETE Method
resource "aws_api_gateway_method" "delete_farmer_service" {
  rest_api_id   = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id   = aws_api_gateway_resource.farmer_service.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_farmer_service" {
  rest_api_id = aws_api_gateway_rest_api.tech4parking_api.id
  resource_id = aws_api_gateway_resource.farmer_service.id
  http_method = aws_api_gateway_method.delete_farmer_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/farmer-service"
  integration_http_method = "DELETE"
}
