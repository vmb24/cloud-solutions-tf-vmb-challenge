resource "aws_api_gateway_deployment" "equipment_health_microservice" {
  depends_on = [
    aws_api_gateway_method.post_equipment_health_service,
    aws_api_gateway_method.get_equipment_health_service,
    aws_api_gateway_method.put_equipment_health_service,
    aws_api_gateway_method.delete_equipment_health_service,
    aws_api_gateway_integration.post_equipment_health_service,
    aws_api_gateway_integration.get_equipment_health_service,
    aws_api_gateway_integration.put_equipment_health_service,
    aws_api_gateway_integration.delete_equipment_health_service
  ]
  rest_api_id = aws_api_gateway_rest_api.equipment_health_microservice.id
  stage_name  = "prod"
}