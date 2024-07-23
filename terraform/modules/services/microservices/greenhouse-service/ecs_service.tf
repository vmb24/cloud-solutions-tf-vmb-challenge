resource "aws_ecs_service" "greenhouse_service" {
  name            = "greenhouse-service"
  cluster         = var.terrafarming_microservices_ecs_cluster_id
  task_definition = aws_ecs_task_definition.greenhouse_service.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets         = [var.private_subnet_id1, var.private_subnet_id2]
    security_groups = [var.ecs_service_sg_id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.greenhouse_service.arn
    container_name   = "greenhouse-service"
    container_port   = 80
  }

  deployment_controller {
    type = "ECS"
  }

  # Configuração de Auto Scaling
  lifecycle {
    ignore_changes = [desired_count]
  }

  depends_on = [
    aws_lb_listener.http
  ]
}