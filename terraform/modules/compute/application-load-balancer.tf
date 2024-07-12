# resource "aws_lb" "ecs_alb" {
#   name               = "terrafarming-alb"
#   internal           = false
#   load_balancer_type = "application"
#   security_groups    = [aws_security_group.ecs_sg.id]
#   subnets            = [var.subnet_id1, var.subnet_id2]

#   enable_deletion_protection = false
# }

# resource "aws_lb_target_group" "ecs_alb_target_group" {
#   name        = "terrafarming-tg"
#   port        = 80
#   protocol    = "HTTP"
#   vpc_id      = var.vpc_id
#   target_type = "instance"
# }

# resource "aws_lb_listener" "ecs_alb_listener" {
#   load_balancer_arn = aws_lb.ecs_alb.arn
#   port              = 80
#   protocol          = "HTTP"

#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.ecs_alb_target_group.arn
#   }

#   lifecycle {
#     prevent_destroy = false
#   }
# }