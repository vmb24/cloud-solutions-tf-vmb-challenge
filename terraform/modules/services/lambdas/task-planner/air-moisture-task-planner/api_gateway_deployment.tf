# Deployment da API Gateway
resource "aws_api_gateway_deployment" "air_moisture_task_planner_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_task_plan
    # aws_api_gateway_integration.lambda_generate_task_plan  # Comentado ou removido
  ]

  rest_api_id = aws_api_gateway_rest_api.air_moisture_task_planner_api.id
  stage_name  = "prod"

  lifecycle {
    create_before_destroy = true
  }

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.air_moisture_task_plan.id,
      aws_api_gateway_resource.generate_task_plan.id,
      aws_api_gateway_method.get_task_plan.id,
      aws_api_gateway_integration.lambda_task_plan.id,
      # Adicione aqui o ID do método e integração para generate_task_plan quando estiverem disponíveis
    ]))
  }
}