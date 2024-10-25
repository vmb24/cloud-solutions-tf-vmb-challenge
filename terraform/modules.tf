module "security" {
  source = "./modules/identity-compliance-security/security"
}

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

  vpc_cidr_block       = var.vpc_cidr_block
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
}

module "compute" {
  source = "./modules/compute"

  aws_region        = var.aws_region
  vpc_id            = module.network.vpc_id
  vpc_cidr_block    = var.vpc_cidr_block
  public_subnet_id1 = module.network.public_subnet_ids[0]
  public_subnet_id2 = module.network.public_subnet_ids[1]
}

module "management_governance" {
  source = "./modules/management-governance"

  ecs_website_service_name     = var.ecs_website_service_name
  ecs_task_execution_role_name = module.general_identity_compliance_security.ecs_task_execution_role_name
  website_load_balancer_arn_suffix = module.compute.website_load_balancer_arn_suffix
  website_lb_target_arn_suffix = module.website.website_lb_target_arn_suffix
}

module "application" {
  source = "./modules/application"

  kms_key_current_arn                         = module.general_identity_compliance_security.kms_key_current_arn
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
  public_subnet_id1 = module.network.public_subnet_ids[0]
  efs_security_group_id = module.compute.efs_security_group_id
}

module "general_identity_compliance_security" {
  source = "./modules/identity-compliance-security/general"

  aws_region = var.aws_region
  ecs_website_service_name = var.ecs_website_service_name

  website_bucket_id = module.storage.website_bucket_id
  website_bucket_name = module.storage.website_bucket_name

  # Processing Lambdas Role IDs
  air_moisture_data_processing_recommendations_lambda_role_id = module.processing_data_lambda_identity_compliance_security.air_moisture_data_processing_recommendations_lambda_role_id
  air_temperature_data_processing_recommendations_lambda_role_id = module.processing_data_lambda_identity_compliance_security.air_temperature_data_processing_recommendations_lambda_role_id
  brightness_data_processing_recommendations_lambda_role_id = module.processing_data_lambda_identity_compliance_security.brightness_data_processing_recommendations_lambda_role_id
  soil_moisture_data_processing_recommendations_lambda_role_id = module.processing_data_lambda_identity_compliance_security.soil_moisture_data_processing_recommendations_lambda_role_id
  soil_temperature_data_processing_recommendations_lambda_role_id = module.processing_data_lambda_identity_compliance_security.soil_temperature_data_processing_recommendations_lambda_role_id

  # Task Planner Lambdas Role IDs
  air_moisture_task_planner_lambda_role_id = module.task_planner_lambda_identity_compliance_security.air_moisture_task_planner_lambda_role_id
  air_temperature_task_planner_lambda_role_id = module.task_planner_lambda_identity_compliance_security.air_temperature_task_planner_lambda_role_id
  brightness_task_planner_lambda_role_id = module.task_planner_lambda_identity_compliance_security.brightness_task_planner_lambda_role_id
  soil_moisture_task_planner_lambda_role_id = module.task_planner_lambda_identity_compliance_security.soil_moisture_task_planner_lambda_role_id
  soil_temperature_task_planner_lambda_role_id = module.task_planner_lambda_identity_compliance_security.soil_temperature_task_planner_lambda_role_id
}

module "users_accounts_identity_compliance_security" {
  source = "./modules/identity-compliance-security/users_accounts"

  users_accounts_table_arn = module.users_accounts_database.users_accounts_table_arn
}

module "analisys_identity_compliance_security" {
  source = "./modules/identity-compliance-security/analisys"
}

module "processing_data_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/processing-lambda-iam"

  aws_region = var.aws_region
}

module "task_planner_lambda_identity_compliance_security" {
  source = "./modules/identity-compliance-security/task-planner-lambda-iam"

  aws_region = var.aws_region
}

# IDENTITY COMPLIANCE SECURITY
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
  brightness_task_planner_lambda_role_name = module.task_planner_lambda_identity_compliance_security.brightness_task_planner_lambda_role_name
  soil_moisture_task_planner_lambda_role_name = module.task_planner_lambda_identity_compliance_security.soil_moisture_task_planner_lambda_role_name
  soil_temperature_task_planner_lambda_role_name = module.task_planner_lambda_identity_compliance_security.soil_temperature_task_planner_lambda_role_name
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

# TASKS MANAGEMENT COMPLIANCE SECURITY
module "tasks_management_identity_compliance_security" {
  source = "./modules/identity-compliance-security/tasks-management-iam"

  aws_region = var.aws_region
}

# DATABASES
module "users_accounts_database" {
  source = "./modules/database/users_accounts"
}

module "ai_agricultural_recommendations_database" {
  source = "./modules/database/ai-agricultural-recommendations"
}

module "average_value_database" {
  source = "./modules/database/average-value"
}

module "average_value_history_database" {
  source = "./modules/database/average-value-history"
}

module "environmental_database" {
  source = "./modules/database/environmental"
}

module "general_database" {
  source = "./modules/database/general"
}

module "task_planner_databases" {
  source = "./modules/database/task-planner"
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
  ecs_website_service_name       = var.ecs_website_service_name
  public_subnet_id1              = module.network.public_subnet_ids[0]
  public_subnet_id2              = module.network.public_subnet_ids[1]
  website_load_balancer_arn      = module.compute.website_load_balancer_arn
  website_load_balancer_dns_name = module.compute.website_load_balancer_dns_name
  ecs_task_execution_role_arn    = module.general_identity_compliance_security.ecs_task_execution_role_arn
  ecs_public_service_sg_id       = module.compute.ecs_public_service_sg
  acm_certificate_cert_arn       = module.content_delivery.acm_certificate_cert_arn
  route53_record_www_record_name = module.content_delivery.route53_record_www_record_name

  terrafarming_website_ecs_cluster_id               = module.application.terrafarming_website_ecs_cluster_id
  terrafarming_website_ecs_cluster_name             = module.application.terrafarming_website_ecs_cluster_name
  website_sg_id                                     = module.compute.website_sg_id
  cloudwatch_log_group_website_container_name       = module.management_governance.cloudwatch_log_group_website_container_name
  cloudwatch_log_group_website_task_definition_name = module.management_governance.cloudwatch_log_group_website_task_definition_name
  website_efs_id = module.storage.website_efs_id
}

# LAMBDAS

# USERS ACCOUNTS LAMBDA
module "users_accounts_lambda" {
  source = "./modules/services/lambdas/users_accounts"

  users_account_name_table = module.users_accounts_database.users_accounts_table_arn
  users_accounts_lambdas_roles_iam_arn = module.users_accounts_identity_compliance_security.users_accounts_lambdas_roles_iam_arn
}

# PROCESSING DATA LAMBDAS
module "air_moisture_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/air-moisture-data-processing-recommendations"

  air_moisture_data_processing_recommendations_lambda_role_arn = module.processing_data_lambda_identity_compliance_security.air_moisture_data_processing_recommendations_lambda_role_arn
  air_moisture_iot_rule_arn                                         = module.internet_of_things.air_moisture_iot_rule_arn
}

module "air_temperature_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/air-temperature-data-processing-recommendations"

  air_temperature_data_processing_recommendations_lambda_role_arn = module.processing_data_lambda_identity_compliance_security.air_temperature_data_processing_recommendations_lambda_role_arn
  air_temperature_iot_rule_arn                                         = module.internet_of_things.air_temperature_iot_rule_arn
}

module "brightness_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/brightness-data-processing-recommendations"

  brightness_data_processing_recommendations_lambda_role_arn = module.processing_data_lambda_identity_compliance_security.brightness_data_processing_recommendations_lambda_role_arn
  brightness_iot_rule_arn                                         = module.internet_of_things.brightness_iot_rule_arn
}

module "soil_moisture_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/soil-moisture-data-processing-recommendations"

  soil_moisture_data_processing_recommendations_lambda_role_arn = module.processing_data_lambda_identity_compliance_security.soil_moisture_data_processing_recommendations_lambda_role_arn
  soil_moisture_iot_rule_arn                                         = module.internet_of_things.soil_moisture_iot_rule_arn
}

module "soil_temperature_data_processing_recommendations" {
  source = "./modules/services/lambdas/processing-data/soil-temperature-data-processing-recommendations"

  soil_temperature_data_processing_recommendations_lambda_role_arn = module.processing_data_lambda_identity_compliance_security.soil_temperature_data_processing_recommendations_lambda_role_arn
  soil_temperature_iot_rule_arn                                         = module.internet_of_things.soil_temperature_iot_rule_arn
}

# TASK PLANNER LAMBDAS
module "air_moisture_task_planner" {
  source = "./modules/services/lambdas/task-planner/air-moisture-task-planner"

  air_moisture_task_planner_lambda_role_arn = module.task_planner_lambda_identity_compliance_security.air_moisture_task_planner_lambda_role_arn
  air_moisture_iot_rule_arn = module.internet_of_things.air_moisture_iot_rule_arn
}

module "air_temperature_task_planner" {
  source = "./modules/services/lambdas/task-planner/air-temperature-task-planner"

  air_temperature_task_planner_lambda_role_arn = module.task_planner_lambda_identity_compliance_security.air_temperature_task_planner_lambda_role_arn
  air_temperature_iot_rule_arn = module.internet_of_things.air_temperature_iot_rule_arn
}

module "brightness_task_planner" {
  source = "./modules/services/lambdas/task-planner/brightness-task-planner"

  brightness_task_planner_lambda_role_arn = module.task_planner_lambda_identity_compliance_security.brightness_task_planner_lambda_role_arn
  brightness_iot_rule_arn = module.internet_of_things.brightness_iot_rule_arn
}

module "soil_moisture_task_planner" {
  source = "./modules/services/lambdas/task-planner/soil-moisture-task-planner"

  soil_moisture_task_planner_lambda_role_arn = module.task_planner_lambda_identity_compliance_security.soil_moisture_task_planner_lambda_role_arn
  soil_moisture_iot_rule_arn = module.internet_of_things.soil_moisture_iot_rule_arn
}

module "soil_temperature_task_planner" {
  source = "./modules/services/lambdas/task-planner/soil-temperature-task-planner"

  soil_temperature_task_planner_lambda_role_arn = module.task_planner_lambda_identity_compliance_security.soil_temperature_task_planner_lambda_role_arn
  soil_temperature_iot_rule_arn = module.internet_of_things.soil_temperature_iot_rule_arn
}

# GENERATE ACCESSIBLE CONTENTS
# FUTURO!!!!

# GENERATE GIFS LAMBDAS
module "generate_gifs_to_air_moisture_metric_lambda" {
  source = "./modules/services/lambdas/generate-gifs/generate-gifs-to-air-moisture-metric"

  generate_gifs_to_air_moisture_metric_lambda_role_arn = module.generate_gifs_lambda_identity_compliance_security.generate_gifs_to_air_moisture_metric_lambda_role_arn
}

module "generate_gifs_to_air_temperature_metric_lambda" {
  source = "./modules/services/lambdas/generate-gifs/generate-gifs-to-air-temperature-metric"

  generate_gifs_to_air_temperature_metric_lambda_role_arn = module.generate_gifs_lambda_identity_compliance_security.generate_gifs_to_air_temperature_metric_lambda_role_arn
}

module "generate_gifs_to_brightness_metric_lambda" {
  source = "./modules/services/lambdas/generate-gifs/generate-gifs-to-brightness-metric"

  generate_gifs_to_brightness_metric_lambda_role_arn = module.generate_gifs_lambda_identity_compliance_security.generate_gifs_to_brightness_metric_lambda_role_arn
}

module "generate_gifs_to_soil_moisture_metric_lambda" {
  source = "./modules/services/lambdas/generate-gifs/generate-gifs-to-soil-moisture-metric"

  generate_gifs_to_soil_moisture_metric_lambda_role_arn = module.generate_gifs_lambda_identity_compliance_security.generate_gifs_to_soil_moisture_metric_lambda_role_arn
}

module "generate_gifs_to_soil_temperature_metric_lambda" {
  source = "./modules/services/lambdas/generate-gifs/generate-gifs-to-soil-temperature-metric"

  generate_gifs_to_soil_temperature_metric_lambda_role_arn = module.generate_gifs_lambda_identity_compliance_security.generate_gifs_to_soil_temperature_metric_lambda_role_arn
}

# GENERATE IMAGE LAMBDAS
module "generate_images_to_air_moisture_metric_lambda" {
  source = "./modules/services/lambdas/generate-images/generate-images-to-air-moisture-metric"

  generate_images_to_air_moisture_metric_lambda_role_arn = module.generate_images_lambda_identity_compliance_security.generate_images_to_air_moisture_metric_lambda_role_arn
  air_moisture_media_bucket_arn = module.media_bucket.air_moisture_media_bucket_arn
}

module "generate_images_to_air_temperature_metric_lambda" {
  source = "./modules/services/lambdas/generate-images/generate-images-to-air-temperature-metric"

  generate_images_to_air_temperature_metric_lambda_role_arn = module.generate_images_lambda_identity_compliance_security.generate_images_to_air_temperature_metric_lambda_role_arn
  air_temperature_media_bucket_arn = module.media_bucket.air_temperature_media_bucket_arn
}

module "generate_images_to_brightness_metric_lambda" {
  source = "./modules/services/lambdas/generate-images/generate-images-to-brightness-metric"
  
  generate_images_to_brightness_metric_lambda_role_arn = module.generate_images_lambda_identity_compliance_security.generate_images_to_brightness_metric_lambda_role_arn
  brightness_media_bucket_arn = module.media_bucket.brightness_media_bucket_arn
}

module "generate_images_to_soil_moisture_metric_lambda" {
  source = "./modules/services/lambdas/generate-images/generate-images-to-soil-moisture-metric"

  generate_images_to_soil_moisture_metric_lambda_role_arn = module.generate_images_lambda_identity_compliance_security.generate_images_to_soil_moisture_metric_lambda_role_arn
  soil_moisture_media_bucket_arn = module.media_bucket.soil_moisture_media_bucket_arn
}

module "generate_images_to_soil_temperature_metric_lambda" {
  source = "./modules/services/lambdas/generate-images/generate-images-to-soil-temperature-metric"

  generate_images_to_soil_temperature_metric_lambda_role_arn = module.generate_images_lambda_identity_compliance_security.generate_images_to_soil_temperature_metric_lambda_role_arn
  soil_temperature_media_bucket_arn = module.media_bucket.soil_temperature_media_bucket_arn
}

# IÁGRIX LAMBDAS FEATURES
# FUTURO!!!!

# TASK MANAGEMENT LAMBDA
# FUTURO!!!!

# Application Integration (Step Functions)
module "application_integration" {
  source = "./modules/application-integration"

  # IAM role arn
  step_function_role_arn = module.general_identity_compliance_security.step_function_role_arn

  # Processing data lambda arn
  air_moisture_data_processing_recommendations_lambda_arn = module.air_moisture_data_processing_recommendations.air_moisture_data_processing_recommendations_lambda_arn
  air_temperature_data_processing_recommendations_lambda_arn = module.air_temperature_data_processing_recommendations.air_temperature_data_processing_recommendations_lambda_arn
  brightness_processing_recommendations_lambda_arn = module.brightness_data_processing_recommendations.brightness_data_processing_recommendations_lambda_arn
  soil_moisture_data_processing_recommendations_lambda_arn = module.soil_moisture_data_processing_recommendations.soil_moisture_data_processing_recommendations_lambda_arn
  soil_temperature_data_processing_recommendations_lambda_arn = module.soil_temperature_data_processing_recommendations.soil_temperature_data_processing_recommendations_lambda_arn

  # Task planner lambda arn
  air_moisture_task_planner_lambda_arn = module.air_moisture_task_planner.air_moisture_task_planner_lambda_arn
  air_temperature_task_planner_lambda_arn = module.air_temperature_task_planner.air_temperature_task_planner_lambda_arn
  brightness_task_planner_lambda_arn = module.brightness_task_planner.brightness_task_planner_lambda_arn
  soil_moisture_task_planner_lambda_arn = module.soil_moisture_task_planner.soil_moisture_task_planner_lambda_arn
  soil_temperature_task_planner_lambda_arn = module.soil_temperature_task_planner.soil_temperature_task_planner_lambda_arn

  # Generate accessible contents lambdas arn
  # FUTURO!!!!

  # Generate gifs lambdas arn
  generate_gifs_to_air_moisture_metric_lambda_arn = module.generate_gifs_to_air_moisture_metric_lambda.generate_gifs_to_air_moisture_metric_lambda_arn
  generate_gifs_to_air_temperature_metric_lambda_arn = module.generate_gifs_to_air_temperature_metric_lambda.generate_gifs_to_air_temperature_metric_lambda_arn
  generate_gifs_to_brightness_metric_lambda_arn = module.generate_gifs_to_brightness_metric_lambda.generate_gifs_to_brightness_metric_lambda_arn
  generate_gifs_to_soil_moisture_metric_lambda_arn = module.generate_gifs_to_soil_moisture_metric_lambda.generate_gifs_to_soil_moisture_metric_lambda_arn
  generate_gifs_to_soil_temperature_metric_lambda_arn = module.generate_gifs_to_soil_temperature_metric_lambda.generate_gifs_to_soil_temperature_metric_lambda_arn

  # Generate images lambdas arn
  generate_images_to_air_moisture_metric_lambda_arn = module.generate_images_to_air_moisture_metric_lambda.generate_images_to_air_moisture_metric_lambda_arn
  generate_images_to_air_temperature_metric_lambda_arn = module.generate_images_to_air_temperature_metric_lambda.generate_images_to_air_temperature_metric_lambda_arn
  generate_images_to_brightness_metric_lambda_arn = module.generate_images_to_brightness_metric_lambda.generate_images_to_brightness_metric_lambda_arn
  generate_images_to_soil_moisture_metric_lambda_arn = module.generate_images_to_soil_moisture_metric_lambda.generate_images_to_soil_moisture_metric_lambda_arn
  generate_images_to_soil_temperature_metric_lambda_arn = module.generate_images_to_soil_temperature_metric_lambda.generate_images_to_soil_temperature_metric_lambda_arn

  # Ágrix assistant main lambdas arn
  # FUTURO!!!!

  # Ágrix assistant features fulfillments lambdas arn
  #FUTURO

  # Ágrix assistant features lambdas arn
  # FUTURO!!!!

  # Task management lambda arn
  # tasks_management_lambda_arn = module.tasks_management_lambda.tasks_management_lambda_arn

  # Tasks results merge lambda arn
  # tasks_results_merge_lambda_arn = module.tasks_results_merge_lambda.tasks_results_merge_lambda_arn
}

# module "analisys" {
#   source = "./modules/analysis"

#   glue_role_arn = module.analisys_identity_compliance_security.glue_role_arn
# }