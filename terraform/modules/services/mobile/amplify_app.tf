resource "aws_amplify_app" "terrafarming_mobile" {
  name              = "TerrafarmingMobileApp"
  repository        = "https://github.com/vmb24/mobile-frontend-vmb-challenge"
  oauth_token       = "github-oauth-token"
  iam_service_role_arn = var.amplify_mobile_service_role_arn
}