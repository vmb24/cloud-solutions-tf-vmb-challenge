output "cloudwatch_log_group_website_container_name" {
    value = aws_cloudwatch_log_group.website_container_log.name
}

output "cloudwatch_log_group_website_task_definition_name" {
    value = aws_cloudwatch_log_group.website_container_task_definition_log.name
}