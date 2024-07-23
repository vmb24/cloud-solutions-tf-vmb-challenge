resource "aws_api_gateway_rest_api" "soil_metrics_microservice" {
  name        = "soil-metrics-microservice"
  description = "Soil Metrics Service API Gateway"
}

resource "aws_api_gateway_resource" "soil_metrics_service" {
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  parent_id   = aws_api_gateway_rest_api.soil_metrics_microservice.root_resource_id
  path_part   = "soil-metrics-service"
}

# POST Method
resource "aws_api_gateway_method" "post_soil_metrics_service" {
  rest_api_id   = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id   = aws_api_gateway_resource.soil_metrics_service.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_soil_metrics_service" {
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id = aws_api_gateway_resource.soil_metrics_service.id
  http_method = aws_api_gateway_method.post_soil_metrics_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/soil-metrics-service"
  integration_http_method = "POST"
}

# GET Method
resource "aws_api_gateway_method" "get_soil_metrics_service" {
  rest_api_id   = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id   = aws_api_gateway_resource.soil_metrics_service.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_soil_metrics_service" {
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id = aws_api_gateway_resource.soil_metrics_service.id
  http_method = aws_api_gateway_method.get_soil_metrics_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/soil-metrics-service"
  integration_http_method = "GET"
}

# PUT Method
resource "aws_api_gateway_method" "put_soil_metrics_service" {
  rest_api_id   = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id   = aws_api_gateway_resource.soil_metrics_service.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "put_soil_metrics_service" {
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id = aws_api_gateway_resource.soil_metrics_service.id
  http_method = aws_api_gateway_method.put_soil_metrics_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/soil-metrics-service"
  integration_http_method = "PUT"
}

# DELETE Method
resource "aws_api_gateway_method" "delete_soil_metrics_service" {
  rest_api_id   = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id   = aws_api_gateway_resource.soil_metrics_service.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_soil_metrics_service" {
  rest_api_id = aws_api_gateway_rest_api.soil_metrics_microservice.id
  resource_id = aws_api_gateway_resource.soil_metrics_service.id
  http_method = aws_api_gateway_method.delete_soil_metrics_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/soil-metrics-service"
  integration_http_method = "DELETE"
}
