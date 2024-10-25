# IAM role arn
variable "step_function_role_arn" {}

# Processing data lambda arn
variable "air_moisture_data_processing_recommendations_lambda_arn" {}
variable "air_temperature_data_processing_recommendations_lambda_arn" {}
variable "brightness_processing_recommendations_lambda_arn" {}
variable "soil_moisture_data_processing_recommendations_lambda_arn" {}
variable "soil_temperature_data_processing_recommendations_lambda_arn" {}

# Task planner lambda arn
variable "air_moisture_task_planner_lambda_arn" {}
variable "air_temperature_task_planner_lambda_arn" {}
variable "brightness_task_planner_lambda_arn" {}
variable "soil_moisture_task_planner_lambda_arn" {}
variable "soil_temperature_task_planner_lambda_arn" {}

# Generate accessible contents lambdas arn
# variable "accessible_image_recognition_lambda_arn" {}
# variable "accessible_text_simplification_lambda_arn" {}
# variable "accessible_text_to_speech_lambda_arn" {}
# variable "accessible_video_caption_lambda_arn" {}
# variable "management_generate_accessible_contents_lambda_arn" {}

# Generate gifs lambdas arn
variable "generate_gifs_to_air_moisture_metric_lambda_arn" {}
variable "generate_gifs_to_air_temperature_metric_lambda_arn" {}
variable "generate_gifs_to_brightness_metric_lambda_arn" {}
variable "generate_gifs_to_soil_moisture_metric_lambda_arn" {}
variable "generate_gifs_to_soil_temperature_metric_lambda_arn" {}

# Generate images lambdas arn
variable "generate_images_to_air_moisture_metric_lambda_arn" {}
variable "generate_images_to_air_temperature_metric_lambda_arn" {}
variable "generate_images_to_brightness_metric_lambda_arn" {}
variable "generate_images_to_soil_moisture_metric_lambda_arn" {}
variable "generate_images_to_soil_temperature_metric_lambda_arn" {}

# Ágrix assistant main lambdas arn
# variable "agrix_interaction_handler_feature_lambda_arn" {}

# Ágrix assistant features fulfillments lambdas arn
# variable "ar_processor_handler_feature_fulfillment_lambda_arn" {}
# variable "compliance_assistance_handler_feature_fulfillment_lambda_arn" {}
# variable "crop_planning_handler_feature_fulfillment_lambda_arn" {}
# variable "dynamic_personlization_handler_feature_fulfillment_lambda_arn" {}
# variable "image_diagnosis_handler_feature_fulfillment_lambda_arn" {}
# variable "knowledge_sharing_handler_feature_fulfillment_lambda_arn" {}
# variable "learning_module_handler_feature_fulfillment_lambda_arn" {}
# variable "marketing_assistant_handler_feature_fulfillment_lambda_arn" {}
# variable "marketplace_handler_feature_fulfillment_lambda_arn" {}
# variable "predictive_analysis_handler_feature_fulfillment_lambda_arn" {}
# variable "report_generator_handler_feature_fulfillment_lambda_arn" {}
# variable "scenario_simulator_handler_feature_fulfillment_lambda_arn" {}
# variable "sustainability_assistant_handler_feature_fulfillment_lambda_arn" {}
# variable "voice_assistant_handler_feature_fulfillment_lambda_arn" {}

# Ágrix assistant features lambdas arn
# variable "ar_processor_handler_feature_lambda_arn" {}
# variable "compliance_assistance_handler_feature_lambda_arn" {}
# variable "crop_planning_handler_feature_lambda_arn" {}
# variable "dynamic_personlization_handler_feature_lambda_arn" {}
# variable "image_diagnosis_handler_feature_lambda_arn" {}
# variable "knowledge_sharing_handler_feature_lambda_arn" {}
# variable "learning_module_handler_feature_lambda_arn" {}
# variable "marketing_assistant_handler_feature_lambda_arn" {}
# variable "marketplace_handler_feature_lambda_arn" {}
# variable "predictive_analysis_handler_feature_lambda_arn" {}
# variable "report_generator_handler_feature_lambda_arn" {}
# variable "scenario_simulator_handler_feature_lambda_arn" {}
# variable "sustainability_assistant_handler_feature_lambda_arn" {}
# variable "voice_assistant_handler_feature_lambda_arn" {}

# Task management lambda arn
# variable "tasks_management_lambda_arn" {}

# Tasks results merge lambda arn
# variable "tasks_results_merge_lambda_arn" {}