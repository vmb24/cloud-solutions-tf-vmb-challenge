# PROVIDERS
resource "aws_cognito_user_pool_client" "userpool_client" {
  name                                 = "userpool-website-client"
  user_pool_id                         = aws_cognito_user_pool.website_cognito_pool.id
#   callback_urls                        = ["https://example.com"]
#   allowed_oauth_flows_user_pool_client = true
#   allowed_oauth_flows                  = ["code", "implicit"]
#   allowed_oauth_scopes                 = ["openid", "email", "profile"]
#   supported_identity_providers         = ["COGNITO"]
#   logout_urls = ["https://yourapp.com/logout"]
}