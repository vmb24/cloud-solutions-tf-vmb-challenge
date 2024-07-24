resource "aws_lb_listener" "website_listener" {
  load_balancer_arn = var.website_load_balancer_arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.website_lb_target.arn
  }
}

