resource "aws_lb" "website_lb" {
  name               = "website-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.website_sg.id]
  subnets            = [var.public_subnet_id1, var.public_subnet_id2]
}