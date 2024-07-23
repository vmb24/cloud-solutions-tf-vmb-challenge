output "microservices_load_balancer_arn" {
  value = aws_lb.microservices_lb.arn
}

output "microservices_load_balancer_dns_name" {
  value = aws_lb.microservices_lb.dns_name
}

output "website_load_balancer_arn" {
  value = aws_lb.website_lb.arn
}

output "website_load_balancer_dns_name" {
  value = aws_lb.website_lb.dns_name
}

output "ecs_service_sg_id" {
  value = aws_security_group.ecs_service_sg.id
}

output "website_sg_id" {
  value = aws_security_group.website_sg.id
}

output "general_public_sg_id" {
  value = aws_security_group.general_public_sg.id
}