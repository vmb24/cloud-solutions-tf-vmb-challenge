output "website_load_balancer_arn" {
  value = aws_lb.website_lb.arn
}

output "website_load_balancer_arn_suffix" {
  value = aws_lb.website_lb.arn_suffix
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

output "efs_security_group_id" {
  value = aws_security_group.efs_sg.id
}