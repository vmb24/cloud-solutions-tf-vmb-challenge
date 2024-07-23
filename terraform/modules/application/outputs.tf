output "terrafarming_microservices_ecs_cluster_id" {
  value = aws_ecs_cluster.terrafarming_microservices_cluster.id
}

output "terrafarming_microservices_ecs_cluster_name" {
  value = aws_ecs_cluster.terrafarming_microservices_cluster.name
}

output "terrafarming_website_ecs_cluster_id" {
  value = aws_ecs_cluster.terrafarming_website_cluster.id
}

output "terrafarming_website_ecs_cluster_name" {
  value = aws_ecs_cluster.terrafarming_website_cluster.name
}