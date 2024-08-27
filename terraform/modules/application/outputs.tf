output "tech4parking_api_ecs_cluster_id" {
  value = aws_ecs_cluster.tech4parking_api_cluster.id
}

output "tech4parking_api_ecs_cluster_name" {
  value = aws_ecs_cluster.tech4parking_api_cluster.name
}

output "tech4parking_website_ecs_cluster_id" {
  value = aws_ecs_cluster.tech4parking_website_cluster.id
}

output "tech4parking_website_ecs_cluster_name" {
  value = aws_ecs_cluster.tech4parking_website_cluster.name
}