# Load Balancer (exemplo com HTTPS listener)
resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = var.website_load_balancer_arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy = "ELBSecurityPolicy-2016-08"
  certificate_arn = var.acm_certificate_cert_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_website_lb_target.arn
  }
}