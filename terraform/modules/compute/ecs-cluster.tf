resource "aws_ecs_cluster" "cluster" {
  name = "llm-metrics-cluster"
}

resource "aws_ecs_task_definition" "task" {
  family                   = "llm-metrics-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "llm-metrics-container"
      image     = "${aws_ecr_repository.repo.repository_url}:latest"
      essential = true
      environment = [
        {
          name  = "AWS_LAMBDA_FUNCTION_HANDLER"
          value = "lambda_function.lambda_handler"
        }
      ]
    }
  ])

  execution_role_arn = var.ecs_task_execution_role
}

resource "aws_ecs_service" "service" {
  name            = "llm-metrics-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1

  network_configuration {
    subnets         = [var.subnet_id1, var.subnet_id2]
    security_groups = [aws_security_group.ecs_sg.id]
  }
}