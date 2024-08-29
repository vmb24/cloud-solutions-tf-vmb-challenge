resource "aws_iot_topic_rule" "moisture_iot_rule" {
  name        = "soil_moisture"
  sql         = "SELECT * FROM 'moisture_sensor'"
  sql_version = "2016-03-23"
  enabled     = true  // Adicione esta linha

  lambda {
    function_arn = var.soil_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.moisture_task_planner_lambda_arn
  }
}