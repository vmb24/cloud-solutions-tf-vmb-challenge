# API Gateway para gerenciamento de vagas
resource "aws_api_gateway_rest_api" "parking_spot_management_api" {
  name = "ParkingSpotManagementAPI"
}

resource "aws_api_gateway_resource" "spots" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  parent_id   = aws_api_gateway_rest_api.parking_spot_management_api.root_resource_id
  path_part   = "spots"
}

resource "aws_api_gateway_method" "create_spot" {
  rest_api_id   = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id   = aws_api_gateway_resource.spots.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "create_spot_integration" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id = aws_api_gateway_resource.spots.id
  http_method = aws_api_gateway_method.create_spot.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.parking_spot_management.invoke_arn
}

resource "aws_api_gateway_method" "list_spots" {
  rest_api_id   = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id   = aws_api_gateway_resource.spots.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "list_spots_integration" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id = aws_api_gateway_resource.spots.id
  http_method = aws_api_gateway_method.list_spots.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.parking_spot_management.invoke_arn
}

resource "aws_api_gateway_resource" "spot" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  parent_id   = aws_api_gateway_resource.spots.id
  path_part   = "{spot_id}"
}

resource "aws_api_gateway_method" "get_spot" {
  rest_api_id   = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id   = aws_api_gateway_resource.spot.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_spot_integration" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id = aws_api_gateway_resource.spot.id
  http_method = aws_api_gateway_method.get_spot.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.parking_spot_management.invoke_arn
}

resource "aws_api_gateway_method" "delete_spot" {
  rest_api_id   = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id   = aws_api_gateway_resource.spot.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_spot_integration" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_management_api.id
  resource_id = aws_api_gateway_resource.spot.id
  http_method = aws_api_gateway_method.delete_spot.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.parking_spot_management.invoke_arn
}