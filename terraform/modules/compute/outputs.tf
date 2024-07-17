output "load_balancer_arn" {
   value = aws_lb.main.arn
}

output "load_balancer_dns_name" {
  value = aws_lb.main.dns_name
}

output "ecs_service_sg_id" {
  value = aws_security_group.ecs_service_sg.id
}