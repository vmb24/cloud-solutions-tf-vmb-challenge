resource "aws_lb_listener" "website_listener" {
  load_balancer_arn = var.website_load_balancer_arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.website_lb_target.arn
  }
}