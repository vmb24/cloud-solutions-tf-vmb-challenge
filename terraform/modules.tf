module "internet_of_things" {
  source = "./modules/internet-of-things"

  aws_region  = var.aws_region

  air_moisture_data_processing_recommendations_lambda_arn = module.air_moisture_data_processing_recommendations.air_moisture_data_processing_recommendations_lambda_arn
  air_temperature_data_processing_recommendations_lambda_arn = module.air_temperature_data_processing_recommendations.air_temperature_data_processing_recommendations_lambda_arn
  brightness_data_processing_recommendations_lambda_arn = module.brightness_data_processing_recommendations.brightness_data_processing_recommendations_lambda_arn
  soil_moisture_data_processing_recommendations_lambda_arn = module.soil_moisture_data_processing_recommendations.soil_moisture_data_processing_recommendations_lambda_arn
  soil_temperature_data_processing_recommendations_lambda_arn = module.soil_temperature_data_processing_recommendations.soil_temperature_data_processing_recommendations_lambda_arn

  air_moisture_task_planner_lambda_arn = module.air_moisture_task_planner.air_moisture_task_planner_lambda_arn
  air_temperature_task_planner_lambda_arn = module.air_temperature_task_planner.air_temperature_task_planner_lambda_arn
  brightness_task_planner_lambda_arn = module.brightness_task_planner.brightness_task_planner_lambda_arn
  soil_moisture_task_planner_lambda_arn = module.soil_moisture_task_planner.soil_moisture_task_planner_lambda_arn
  soil_temperature_task_planner_lambda_arn = module.soil_temperature_task_planner.soil_temperature_task_planner_lambda_arn
}

module "network" {
  source = "./modules/network"

  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
}

module "compute" {
  source = "./modules/compute"

  aws_region        = var.aws_region
  vpc_id            = module.network.vpc_id
  public_subnet_id1 = module.network.public_subnet_ids[0]
  public_subnet_id2 = module.network.public_subnet_ids[1]
}

module "management_governance" {
  source = "./modules/management-governance"

  ecs_website_service_name     = var.ecs_website_service_name
  ecs_task_execution_role_name = module.identity_compliance_security.ecs_task_execution_role_name
}

module "application" {
  source = "./modules/application"

  kms_key_current_arn                         = module.identity_compliance_security.kms_key_current_arn
  ecs_website_service_name                    = var.ecs_website_service_name
  cloudwatch_log_group_website_container_name = module.management_governance.cloudwatch_log_group_website_container_name
}

module "content_delivery" {
  source = "./modules/content-delivery"

  aws_region                     = var.aws_region
  website_load_balancer_dns_name = module.compute.website_load_balancer_dns_name
  website_bucket_name            = module.storage.website_bucket_name
  website_lb_zone_id             = module.compute.website_lb_zone_id
  website_lb_id                  = module.compute.website_lb_id
}

module "storage" {
  source = "./modules/storage"

  bucket_name = var.bucket_name
  environment = var.environment
}

module "general_identity_compliance_security" {
  source = "./modules/identity-compliance-security/general"

  aws_region = var.aws_region
  ecs_website_service_name = var.ecs_website_service_name

  website_bucket_id = module.storage.website_bucket_id
  website_bucket_name = module.storage.website_bucket_name
}

module "processing_data_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/processing-lambda-iam"

  aws_region = var.aws_region
}

module "task_planner_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/task-planner-lambda-iam"

  aws_region = var.aws_region
}

module "iot_thing_shadow_processing_data_identity_compliance_security" {
  source = "./modules/identity-compliance-security/iot-thing-shadow/processing-data"

  aws_region = var.aws_region
  air_moisture_data_processing_recommendations_lambda_role_name = module.processing_data_lambda_identity_compliance_security.air_moisture_data_processing_recommendations_lambda_role_name
  air_temperature_data_processing_recommendations_lambda_role_name = module.processing_data_lambda_identity_compliance_security.air_temperature_data_processing_recommendations_lambda_role_name
  brightness_data_processing_recommendations_lambda_role_name = module.processing_data_lambda_identity_compliance_security.brightness_data_processing_recommendations_lambda_role_name
  soil_moisture_data_processing_recommendations_lambda_role_name = module.processing_data_lambda_identity_compliance_security.soil_moisture_data_processing_recommendations_lambda_role_name
  soil_temperature_data_processing_recommendations_lambda_role_name = module.processing_data_lambda_identity_compliance_security.soil_temperature_data_processing_recommendations_lambda_role_name
}

module "iot_thing_shadow_task_planner_identity_compliance_security" {
  source = "./modules/identity-compliance-security/iot-thing-shadow/task-planner"

  aws_region = var.aws_region
  air_moisture_task_planner_lambda_role_name = module.task_planner_lambda_identity_compliance_security.air_moisture_task_planner_lambda_role_name
  air_temperature_task_planner_lambda_role_name = module.task_planner_lambda_identity_compliance_security.air_temperature_task_planner_lambda_role_name
  brightness_task_planner_lambda_role_name = module.task_planner_identity_lambda_compliance_security.brightness_task_planner_lambda_role_name
  soil_moisture_task_planner_lambda_role_name = module.task_planner_identity_lambda_compliance_security.soil_moisture_task_planner_lambda_role_name
  soil_temperature_task_planner_lambda_role_name = module.task_planner_identity_lambda_compliance_security.soil_temperature_task_planner_lambda_role_name
}

module "generate_images_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/media/images"

  air_moisture_media_bucket_arn = module.media_bucket.air_moisture_media_bucket_arn
  air_temperature_media_bucket_arn = module.media_bucket.air_temperature_media_bucket_arn
  brightness_media_bucket_arn = module.media_bucket.brightness_media_bucket_arn
  soil_moisture_media_bucket_arn = module.media_bucket.soil_moisture_media_bucket_arn
  soil_temperature_media_bucket_arn = module.media_bucket.soil_temperature_media_bucket_arn
}

module "generate_gifs_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/media/gifs"


  air_moisture_media_bucket_arn = module.media_bucket.air_moisture_media_bucket_arn
  air_temperature_media_bucket_arn = module.media_bucket.air_temperature_media_bucket_arn
  brightness_media_bucket_arn = module.media_bucket.brightness_media_bucket_arn
  soil_moisture_media_bucket_arn = module.media_bucket.soil_moisture_media_bucket_arn
  soil_temperature_media_bucket_arn = module.media_bucket.soil_temperature_media_bucket_arn
}

module "agrix_features_identity_compliance_security" {
  source = "./modules/identity-compliance-security/agrix-assistent/agrix-features"
}

# Ágrix Assistent Features
# TALVEZ ESSA FUNÇÃO SÓ EXISTA NO FUTURO
module "advanced_sensor_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/advanced-sensor-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "ar_processor_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/ar-processor-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "compliance_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/compliance-assistant-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "crop_planning_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/crop-planning-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "dynamic_personalization_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/dynamic-personalization-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "image_diagnosis_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/image-diagnosis-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "knowledge_sharing_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/knowledge-sharing-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "learning_module_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/learning-module-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "marketing_assistant_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/marketing-assistant-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "marketplace_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/marketplace-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "predictive_analysis_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/predictive-analysis-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "scenario_simulator_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/scenario-simulator-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "sustainability_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/sustainability-assistant-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

module "voice_assistant_feature_lambda_handler" {
  source = "./modules/services/lambdas/agrix-assistant/agrix-features/voice-assistant-handler"

  agrix_interaction_lambdas_roles_iam_arn = module.agrix_features_identity_compliance_security.agrix_interaction_lambdas_roles_iam_arn
}

# Processing data lambdas
module "application_integration" {
  source = "./modules/application-integration"
}

module "air_moisture_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/air-moisture-data-processing-recommendations"

  air_moisture_data_processing_recommendations_lambda_role_arn = module.identity_compliance_security.air_moisture_data_processing_recommendations_lambda_role_arn
  air_moisture_iot_rule_arn                                         = module.internet_of_things.air_moisture_iot_rule_arn
}

module "air_temperature_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/air-temperature-data-processing-recommendations"

  air_temperature_data_processing_recommendations_lambda_role_arn = module.identity_compliance_security.air_temperature_data_processing_recommendations_lambda_role_arn
  air_temperature_iot_rule_arn                                         = module.internet_of_things.air_temperature_iot_rule_arn
}

module "brightness_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/brightness-data-processing-recommendations"

  brightness_data_processing_recommendations_lambda_role_arn = module.identity_compliance_security.brightness_data_processing_recommendations_lambda_role_arn
  brightness_iot_rule_arn                                         = module.internet_of_things.brightness_iot_rule_arn
}

module "soil_moisture_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/soil-moisture-data-processing-recommendations"

  soil_moisture_data_processing_recommendations_lambda_role_arn = module.identity_compliance_security.soil_moisture_data_processing_recommendations_lambda_role_arn
  soil_moisture_iot_rule_arn                                         = module.internet_of_things.soil_moisture_iot_rule_arn
}

module "soil_temperature_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/soil-temperature-data-processing-recommendations"

  soil_temperature_data_processing_recommendations_lambda_role_arn = module.identity_compliance_security.soil_temperature_data_processing_recommendations_lambda_role_arn
  soil_temperature_iot_rule_arn                                         = module.internet_of_things.soil_temperature_iot_rule_arn
}

# Task planner processing lambdas
module "air_moisture_task_planner" {
  source = "./modules/services/lambdas/task-planner/air-moisture-task-planner"

  air_moisture_task_planner_lambda_role_arn = module.identity_compliance_security.air_moisture_data_processing_recommendations_lambda_role_arn
  air_moisture_iot_rule_arn = module.internet_of_things.air_moisture_iot_rule_arn
}

module "air_temperature_task_planner" {
  source = "./modules/services/lambdas/task-planner/air-temperature-task-planner"

  air_temperature_task_planner_lambda_role_arn = module.identity_compliance_security.air_temperature_data_processing_recommendations_lambda_role_arn
  air_temperature_iot_rule_arn = module.internet_of_things.air_temperature_iot_rule_arn
}

module "brightness_task_planner" {
  source = "./modules/services/lambdas/task-planner/brightness-task-planner"

  brightness_task_planner_lambda_role_arn = module.identity_compliance_security.brightness_data_processing_recommendations_lambda_role_arn
  brightness_iot_rule_arn = module.internet_of_things.brightness_iot_rule_arn
}

module "soil_moisture_task_planner" {
  source = "./modules/services/lambdas/task-planner/soil-moisture-task-planner"

  soil_moisture_task_planner_lambda_role_arn = module.identity_compliance_security.soil_moisture_data_processing_recommendations_lambda_role_arn
  soil_moisture_iot_rule_arn = module.internet_of_things.soil_moisture_iot_rule_arn
}

module "soil_temperature_task_planner" {
  source = "./modules/services/lambdas/task-planner/soil-temperature-task-planner"

  soil_temperature_task_planner_lambda_role_arn = module.identity_compliance_security.soil_temperature_data_processing_recommendations_lambda_role_arn
  soil_temperature_iot_rule_arn = module.internet_of_things.soil_temperature_iot_rule_arn
}

# Databases
module "ai_agricultural_recommendations_database" {
  source = "./modules/database/ai-agricultural-recommendations"
}

module "average_value_database" {
  source = "./modules/database/average-value"
}

module "average_value_history_database" {
  source = "./modules/database/average-value"
}

module "environmental_database" {
  source = "./modules/database/environmental"
}

module "general_database" {
  source = "./modules/database/general"
}

# Media databases
module "media_database" {
  source = "./modules/database/media"
}

# Media buckets
module "media_bucket" {
  source = "./modules/storage/media"
}

# Website resources
module "website" {
  source = "./modules/services/website"

  aws_region                     = var.aws_region
  vpc_id                         = module.network.vpc_id
  public_subnet_id1              = module.network.public_subnet_ids[0]
  public_subnet_id2              = module.network.public_subnet_ids[1]
  website_load_balancer_arn      = module.compute.website_load_balancer_arn
  website_load_balancer_dns_name = module.compute.website_load_balancer_dns_name
  ecs_task_execution_role_arn    = module.identity_compliance_security.ecs_task_execution_role_arn
  ecs_public_service_sg_id       = module.compute.ecs_public_service_sg
  acm_certificate_cert_arn       = module.content_delivery.acm_certificate_cert_arn
  route53_record_www_record_name = module.content_delivery.route53_record_www_record_name

  terrafarming_website_ecs_cluster_id               = module.application.terrafarming_website_ecs_cluster_id
  terrafarming_website_ecs_cluster_name             = module.application.terrafarming_website_ecs_cluster_name
  website_sg_id                                     = module.compute.website_sg_id
  cloudwatch_log_group_website_container_name       = module.management_governance.cloudwatch_log_group_website_container_name
  cloudwatch_log_group_website_task_definition_name = module.management_governance.cloudwatch_log_group_website_task_definition_name
}