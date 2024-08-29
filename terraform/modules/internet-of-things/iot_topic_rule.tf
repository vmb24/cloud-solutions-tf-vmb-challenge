resource "aws_iot_topic_rule" "parking_iot_rule" {
  name        = "parking_sensor"
  sql         = "SELECT * FROM 'parking_sensor'"
  sql_version = "2016-03-23"
  enabled     = true  // Adicione esta linha

  lambda {
    function_arn = var.parking_spot_management_lambda_arn
  }

  lambda {
    function_arn = var.parking_spot_status_update_lambda_arn
  }
}
