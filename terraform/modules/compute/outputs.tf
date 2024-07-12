output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.repo.repository_url
}

# output "lb_dns_name" {
#   value = aws_lb.ecs_alb.dns_name
# }

# output "target_group_arn" {
#   value = aws_lb_target_group.ecs_alb_target_group.arn
# }