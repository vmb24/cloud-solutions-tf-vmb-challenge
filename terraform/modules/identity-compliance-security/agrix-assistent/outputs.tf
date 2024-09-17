# ESSA PRÁTICA NÃO É RECOMENDADA!!!!! CADA FUNÇÃO DEVE TER SUAS PRÓPRIAS PERMISSÕES!!! Será alterado no futuro.
output "agrix_interaction_handler_lambdas_roles_iam_arn" {
  value = aws_iam_role.agrix_interaction_handler_lambda_role.arn
}