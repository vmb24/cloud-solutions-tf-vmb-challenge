resource "aws_ecs_task_definition" "farmer_service" {
  family                   = "farmer-service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "farmer-service"
      image     = "${aws_ecr_repository.farmer_service.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        {
          name  = "DYNAMODB_TABLE"
          value = "Farmers"
        },
        {
          name  = "AWS_REGION"
          value = var.aws_region
        }
      ]
    }
  ])

  execution_role_arn = var.ecs_task_execution_role_arn
  task_role_arn      = var.ecs_task_execution_role_arn
}