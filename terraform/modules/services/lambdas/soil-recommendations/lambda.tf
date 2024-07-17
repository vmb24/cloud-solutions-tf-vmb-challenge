resource "aws_lambda_function" "llm_soil_recommendations" {
  function_name = "llm-soil-recommendations-lambda"
  role          = var.iam_role_lambda_exec_arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.soil_recommendations_lambda.repository_url}:latest"
  timeout       = 300
}
