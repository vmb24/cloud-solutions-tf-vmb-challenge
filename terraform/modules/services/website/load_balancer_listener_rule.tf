resource "aws_lb_listener_rule" "example" {
  listener_arn = aws_lb_listener.website_listener_lb_http.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.website_lb_target.arn
  }

  condition {
    host_header {
      values = ["terrafarming.com.br"]
    }
  }
}
