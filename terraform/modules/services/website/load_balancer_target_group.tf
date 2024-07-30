resource "aws_lb_target_group" "website_lb_target" {
  name     = "website-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  # Defina o tipo de destino como "ip"
  target_type = "ip"

  health_check {
    path                = "/api/health"  # Caminho do endpoint de verificação de saúde
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}