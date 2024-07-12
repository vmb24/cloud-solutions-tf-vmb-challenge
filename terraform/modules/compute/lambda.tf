resource "aws_lambda_function" "llm_metrics" {
  function_name = "llm-metrics-lambda"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.repo.repository_url}:latest"
  timeout       = 300
}
