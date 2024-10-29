resource "aws_cloudwatch_log_group" "website_container_log" {
  name              = "/aws/ecs/${var.ecs_website_service_name}"
  retention_in_days = 7
  tags = {
	Terraform = "true"
	Name = "cloudwatch-group-${var.ecs_website_service_name}"
  }
}

resource "aws_cloudwatch_log_group" "website_container_task_definition_log" {
  name              = "/aws/ecs/${var.ecs_website_service_name}/task_definition_logs"
  retention_in_days = 7
  tags = {
	Terraform = "true"
	Name = "cloudwatch-group-${var.ecs_website_service_name}-task-definition"
  }
}

data "aws_iam_policy_document" "cloudwatch_logs_policy" {
  statement {
	actions = [
	  "logs:CreateLogStream",
	  "logs:CreateLogGroup",
	  "logs:DescribeLogStreams",
	  "logs:PutLogEvents"
	]

    resources = [
      "${aws_cloudwatch_log_group.website_container_log.arn}",
      "${aws_cloudwatch_log_group.website_container_task_definition_log.arn}"
    ]
  }
}

resource "aws_iam_policy" "cloudwatch_logs_policy" {
  path   = "/ecs/task-role/"
  policy = data.aws_iam_policy_document.cloudwatch_logs_policy.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_logs_policy" {
  role       = var.ecs_task_execution_role_name
  policy_arn = aws_iam_policy.cloudwatch_logs_policy.arn
}