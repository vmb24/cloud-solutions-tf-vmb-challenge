resource "aws_lb_listener" "website_listener_lb_http" {
  load_balancer_arn = var.website_load_balancer_arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      protocol = "HTTPS"
      port     = "443"
      status_code = "HTTP_301"
    }
  }
}
