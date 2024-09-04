resource "aws_lb_listener_rule" "website_lb_listener_rule" {
  listener_arn = aws_lb_listener.https_listener.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_website_lb_target.arn
  }

  condition {
    host_header {
      values = ["terrafarming.com.br"]
    }
  }
}