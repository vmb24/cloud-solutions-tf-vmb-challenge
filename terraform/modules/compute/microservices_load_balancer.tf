resource "aws_lb" "microservices_lb" {
  name               = "microservices-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_public_service_sg.id]
  subnets            = [var.public_subnet_id1, var.public_subnet_id2]
}