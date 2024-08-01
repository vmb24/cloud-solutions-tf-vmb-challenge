resource "aws_lb" "website_lb" {
  name               = "website-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.website_sg.id]
  subnets            = [var.public_subnet_id1, var.public_subnet_id2]
  enable_deletion_protection = false
  enable_cross_zone_load_balancing = true
  enable_http2 = true

  # # VERIFICAR
  # access_logs {
  #     bucket  = var.load_balancer_logging_bucket
  #     prefix  = "load-balancer-logs"
  #     enabled = true
  # }
}