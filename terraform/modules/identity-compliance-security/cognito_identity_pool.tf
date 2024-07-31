resource "aws_cognito_identity_pool" "cognito_website_providers" {
  identity_pool_name = "my-identity-pool"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    provider_name = aws_cognito_user_pool.website_cognito_pool.endpoint
    client_id     = aws_cognito_user_pool_client.userpool_client.id
  }
}
