resource "aws_ecs_task_definition" "ecs_website_task" {
  family                   = "ecs-website-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"  # 1 vCPU
  memory                   = "2048"  # 2 GB
  execution_role_arn       = var.ecs_task_execution_role_arn

  volume {
    name = "website-storage"
    efs_volume_configuration {
      file_system_id = var.website_efs_id
      root_directory = "/"
    }
  }

  container_definitions    = jsonencode([
    {
      name      = "website"
      image     = "${aws_ecr_repository.terrafarming_website_repo.repository_url}:latest"
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
      mountPoints = [
        {
          sourceVolume  = "website-storage",
          containerPath = "/app/storage"  # Ajuste conforme necessário
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