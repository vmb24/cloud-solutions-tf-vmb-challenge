# API Gateway para atualização de status de vagas
resource "aws_api_gateway_rest_api" "parking_spot_status_api" {
  name = "ParkingSpotStatusAPI"
}

resource "aws_api_gateway_resource" "status" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_status_api.id
  parent_id   = aws_api_gateway_rest_api.parking_spot_status_api.root_resource_id
  path_part   = "spots"
}

resource "aws_api_gateway_resource" "spot_id" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_status_api.id
  parent_id   = aws_api_gateway_resource.status.id
  path_part   = "{spot_id}"
}

resource "aws_api_gateway_resource" "status_update" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_status_api.id
  parent_id   = aws_api_gateway_resource.spot_id.id
  path_part   = "status"
}

resource "aws_api_gateway_method" "update_status" {
  rest_api_id   = aws_api_gateway_rest_api.parking_spot_status_api.id
  resource_id   = aws_api_gateway_resource.status_update.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "update_status_integration" {
  rest_api_id = aws_api_gateway_rest_api.parking_spot_status_api.id
  resource_id = aws_api_gateway_resource.status_update.id
  http_method = aws_api_gateway_method.update_status.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.parking_spot_status_update.invoke_arn
}