resource "aws_api_gateway_rest_api" "equipment_health_microservice" {
  name        = "equipment-health-microservice"
  description = "Equipment Health Service API Gateway"
}

resource "aws_api_gateway_resource" "equipment_health_service" {
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  parent_id   = aws_api_gateway_rest_api.equipment_health_microservice.root_resource_id
  path_part   = "equipment-health-service"
}

# POST Method
resource "aws_api_gateway_method" "post_equipment_health_service" {
  rest_api_id   = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id   = aws_api_gateway_resource.equipment_health_service.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_equipment_health_service" {
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id = aws_api_gateway_resource.equipment_health_service.id
  http_method = aws_api_gateway_method.post_equipment_health_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/equipment-health-service"
  integration_http_method = "POST"
}

# GET Method
resource "aws_api_gateway_method" "get_equipment_health_service" {
  rest_api_id   = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id   = aws_api_gateway_resource.equipment_health_service.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_equipment_health_service" {
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id = aws_api_gateway_resource.equipment_health_service.id
  http_method = aws_api_gateway_method.get_equipment_health_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/equipment-health-service"
  integration_http_method = "GET"
}

# PUT Method
resource "aws_api_gateway_method" "put_equipment_health_service" {
  rest_api_id   = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id   = aws_api_gateway_resource.equipment_health_service.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "put_equipment_health_service" {
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id = aws_api_gateway_resource.equipment_health_service.id
  http_method = aws_api_gateway_method.put_equipment_health_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/equipment-health-service"
  integration_http_method = "PUT"
}

# DELETE Method
resource "aws_api_gateway_method" "delete_equipment_health_service" {
  rest_api_id   = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id   = aws_api_gateway_resource.equipment_health_service.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_equipment_health_service" {
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  resource_id = aws_api_gateway_resource.equipment_health_service.id
  http_method = aws_api_gateway_method.delete_equipment_health_service.http_method
  type        = "HTTP"
  uri         = "http://${var.microservices_load_balancer_dns_name}/equipment-health-service"
  integration_http_method = "DELETE"
}
