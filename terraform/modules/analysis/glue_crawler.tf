# resource "aws_glue_crawler" "dynamodb_crawler" {
#   for_each      = toset([
#     "air_moisture_history",
#     "air_temperature_history",
#     "brightness_history",
#     "soil_moisture_history",
#     "soil_temperature_history",
#     "ai_agricultural_air_moisture_recommendations",
#     "ai_agricultural_air_temperature_recommendations",
#     "ai_agricultural_brightness_recommendations",
#     "ai_agricultural_soil_moisture_recommendations",
#     "ai_agricultural_soil_temperature_recommendations",
#     "ai_air_moisture_task_plans",
#     "ai_air_temperature_task_plans",
#     "ai_brightness_task_plans",
#     "ai_soil_moisture_task_plans",
#     "ai_soil_temperature_task_plans"
#   ])

#   name          = "${each.key}-crawler"
#   database_name = "agricultural_data"
#   role          = var.glue_role_arn

#   dynamodb_target {
#     path = each.key
#   }
# }