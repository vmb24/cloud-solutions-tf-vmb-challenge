# resource "aws_launch_configuration" "ecs_launch_configuration" {
#   name          = "ecs-launch-configuration"
#   image_id      = data.aws_ami.amazon_linux.id
#   instance_type = "t2.micro"
#   iam_instance_profile = var.ecs_task_execution_role

#   lifecycle {
#     create_before_destroy = true
#   }

#   root_block_device {
#     volume_size = 8
#     volume_type = "gp2"
#   }

#   security_groups = [aws_security_group.ecs_sg.id]
# }

# resource "aws_autoscaling_group" "ecs_autoscaling" {
#   desired_capacity     = 1
#   max_size             = 2
#   min_size             = 1
#   vpc_zone_identifier  = var.public_subnet_ids
#   launch_configuration = aws_launch_configuration.ecs_launch_configuration.id

#   target_group_arns = [aws_lb_target_group.ecs_alb_target_group.arn]

#   tag {
#     key                 = "Name"
#     value               = "ecs-instance"
#     propagate_at_launch = true
#   }
# }