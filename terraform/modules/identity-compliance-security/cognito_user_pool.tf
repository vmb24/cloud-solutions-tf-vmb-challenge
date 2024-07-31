resource "aws_cognito_user_pool" "website_cognito_pool" {
  name = "website-cognito-pool"

  auto_verified_attributes = ["email"]

  mfa_configuration = "OFF"

  password_policy {
    minimum_length    = 8
    require_numbers   = true
    require_lowercase = true
    require_uppercase = true
    require_symbols   = true
  }
}