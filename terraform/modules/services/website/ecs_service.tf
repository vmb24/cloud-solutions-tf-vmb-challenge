resource "aws_ecs_service" "website_service" {
  name            = "website-service"
  cluster         = var.tech4parking_website_ecs_cluster_id
  task_definition = aws_ecs_task_definition.ecs_website_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [var.public_subnet_id1, var.public_subnet_id2]
    security_groups  = [var.website_sg_id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app_website_lb_target.arn
    container_name   = "website"
    container_port   = 3000
  }

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Name = "website-service"
  }
}