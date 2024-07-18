resource "aws_amplify_app" "terrafarming_mobile" {
  name              = "TerrafarmingMobileApp"
  repository        = "https://github.com/username/my-react-native-app"
  oauth_token       = "github-oauth-token"
  iam_service_role_arn = var.amplify_mobile_service_role_arn
}