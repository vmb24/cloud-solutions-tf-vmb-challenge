resource "aws_ecs_task_definition" "ecs_website_task" {
  family                   = "ecs-website-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = var.ecs_task_execution_role_arn
  container_definitions    = jsonencode([
    {
      name      = "website"
      image     = "${aws_ecr_repository.tech4parking_website_repo.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 3000
          hostPort      = 3000
        }
      ]
      environment = [
        {
          name  = "NODE_ENV"
          value = "production"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "${var.cloudwatch_log_group_website_task_definition_name}"
          "awslogs-region"        = "us-east-1" # Substitua pela sua região
          "awslogs-stream-prefix" = "website"
        }
      }
    }
  ])
}