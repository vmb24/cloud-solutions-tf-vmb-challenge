output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "iam_role_lambda_exec_arn" {
  value = aws_iam_role.lambda_exec.arn
}

output "amplify_mobile_service_role_arn" {
  value = aws_iam_role.amplify_mobile_service_role.arn
}

output "kms_key_current_arn" {
  value = aws_kms_key.current.arn
}

output "ecs_task_execution_role_name" {
  value = aws_iam_role.ecs_task_execution_role.name
}

output "cognito_website_providers_id" {
  value = aws_cognito_identity_pool.cognito_website_providers.id
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.website_cognito_pool.id
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.userpool_client.id
}

output "cognito_user_pool_client_arn" {
  value = aws_cognito_user_pool.website_cognito_pool.arn
}