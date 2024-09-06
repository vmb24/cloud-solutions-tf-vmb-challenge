resource "aws_iot_topic_rule" "soil_moisture_rule" {
  name        = "soil_moisture_rule"
  sql         = "SELECT * FROM 'agriculture/soil/moisture'"
  sql_version = "2016-03-23"
  enabled     = true

  lambda {
    function_arn = var.soil_moisture_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.soil_moisture_task_planner_lambda_arn
  }
}

resource "aws_iot_topic_rule" "soil_temperature_rule" {
  name        = "soil_temperature_rule"
  sql         = "SELECT * FROM 'agriculture/soil/temperature'"
  sql_version = "2016-03-23"
  enabled     = true

  lambda {
    function_arn = var.soil_temperature_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.soil_temperature_task_planner_lambda_arn
  }
}

resource "aws_iot_topic_rule" "air_moisture_rule" {
  name        = "air_moisture_rule"
  sql         = "SELECT * FROM 'agriculture/air/moisture'"
  sql_version = "2016-03-23"
  enabled     = true

  lambda {
    function_arn = var.air_moisture_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.air_moisture_task_planner_lambda_arn
  }
}

resource "aws_iot_topic_rule" "air_temperature_rule" {
  name        = "air_temperature_rule"
  sql         = "SELECT * FROM 'agriculture/air/temperature'"
  sql_version = "2016-03-23"
  enabled     = true

  lambda {
    function_arn = var.air_temperature_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.air_temperature_task_planner_lambda_arn
  }
}

resource "aws_iot_topic_rule" "brightness_rule" {
  name        = "brightness_rule"
  sql         = "SELECT * FROM 'agriculture/brightness'"
  sql_version = "2016-03-23"
  enabled     = true

  lambda {
    function_arn = var.brightness_data_processing_recommendations_lambda_arn
  }

  lambda {
    function_arn = var.brightness_task_planner_lambda_arn
  }
}