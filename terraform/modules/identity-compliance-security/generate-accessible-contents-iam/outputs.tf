# ESSA PRÁTICA NÃO É RECOMENDADA!!!!! CADA FUNÇÃO DEVE TER SUAS PRÓPRIAS PERMISSÕES!!! Será alterado no futuro.

output "accessible_image_recognition_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.accessible_image_recognition_handler_lambda_role.arn
}

output "accessible_text_simplification_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.accessible_text_simplification_handler_lambda_role.arn
}

output "accessible_text_to_speech_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.accessible_text_to_speech_handler_lambda_role.arn
}

output "accessible_video_captions_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.accessible_video_caption_handler_lambda_role.arn
}

output "management_generate_accessible_contents_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.management_generate_accessible_contents_handler_lambda_role.arn
}
