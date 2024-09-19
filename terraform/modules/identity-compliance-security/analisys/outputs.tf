output "quicksight_athena_access_role_arn" {
  value = aws_iam_role.quicksight_athena_access.arn
}

output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}