resource "aws_lb_target_group" "app_website_lb_target" {
  name     = "app-website-target-group"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  target_type = "ip"
  deregistration_delay = 30

  health_check {
    path                = "/api/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}