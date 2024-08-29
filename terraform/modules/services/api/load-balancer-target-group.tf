# Target Group for Farmer Service
resource "aws_lb_target_group" "farmer_service" {
  name     = "farmer-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  target_type = "ip"  # Definindo o tipo de alvo como "ip" para suportar contêineres ECS Fargate

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }

  tags = {
    Name = "farmer-service-target-group"
  }
}
