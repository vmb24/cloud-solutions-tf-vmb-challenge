output "api_load_balancer_arn" {
  value = aws_lb.api_lb.arn
}

output "api_load_balancer_dns_name" {
  value = aws_lb.api_lb.dns_name
}

output "website_load_balancer_arn" {
  value = aws_lb.website_lb.arn
}

output "website_load_balancer_dns_name" {
  value = aws_lb.website_lb.dns_name
}

output "ecs_public_service_sg" {
  value = aws_security_group.ecs_public_service_sg.id
}

output "website_sg_id" {
  value = aws_security_group.website_sg.id
}

output "general_public_sg_id" {
  value = aws_security_group.general_public_sg.id
}

output "website_lb_zone_id" {
  value = aws_lb.website_lb.zone_id
}

output "website_lb_id" {
  value = aws_lb.website_lb.id
}

# output "autoscaling_group_web_asg_name" {
#   value = aws_autoscaling_group.web_asg.name
# }

# output "website_autoscaling_group_name" {
#   value = aws_autoscaling_group.web_asg.name
# }