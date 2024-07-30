module "identity_compliance_security" {
  source = "./modules/identity-compliance-security"

  ecs_website_service_name = var.ecs_website_service_name
  website_bucket_id        = module.storage.website_bucket_id
  website_bucket_name      = module.storage.website_bucket_name
  # cloudfront_oai_id = module.content_delivery.cloudfront_oai_id
  logging_bucket_arn = module.storage.logging_bucket_arn
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

  aws_region         = var.aws_region
  vpc_id             = module.network.vpc_id
  public_subnet_id1  = module.network.public_subnet_ids[0]
  public_subnet_id2  = module.network.public_subnet_ids[1]
  private_subnet_id1 = module.network.private_subnet_ids[0]
  private_subnet_id2 = module.network.private_subnet_ids[1]
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

  website_load_balancer_dns_name      = module.compute.website_load_balancer_dns_name
  acm_certificate_cert_arn            = var.acm_certificate_cert_arn
  website_bucket_name                 = module.storage.website_bucket_name
  website_bucket_regional_domain_name = module.storage.website_bucket_regional_domain_name
  logging_bucket_name                 = module.storage.logging_bucket_name
}

module "storage" {
  source = "./modules/storage"

  bucket_name = var.bucket_name
  environment = var.environment
}

# module "database" {
#   source = "./modules/database"
# }

# module "farmer_service" {
#   source = "./modules/services/microservices/farmer-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name
#   sns_topic_soil_metrics_notifications_arn = module.soil_metrics_service.sns_topic_soil_metrics_notifications_arn
#   sns_topic_weather_notifications_arn = module.weather_service.sns_topic_weather_notifications_arn
#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "soil_metrics_service" {
#   source = "./modules/services/microservices/soil-metrics-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name 
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn
#   sns_topic_equipment_health_notifications_arn = module.equipment_health_service.sns_topic_equipment_health_notifications_arn

#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "crop_health_service" {
#   source = "./modules/services/microservices/crop-health-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
#   sns_topic_greenhouse_notifications_arn = module.greenhouse_service.sns_topic_greenhouse_notifications_arn

#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "equipment_health_service" {
#   source = "./modules/services/microservices/equipment-health-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name
#   sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
#   sns_topic_soil_metrics_notifications_arn = module.soil_metrics_service.sns_topic_soil_metrics_notifications_arn

#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "weather_service" {
#   source = "./modules/services/microservices/weather-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_weather_recommendation_notifications_arn = module.weather_recommendations_lambda.sns_topic_weather_recommendation_notifications_arn
#   sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn

#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "greenhouse_service" {
#   source = "./modules/services/microservices/greenhouse-service"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_public_service_sg_id           = module.compute.ecs_public_service_sg_id

#   terrafarming_microservices_ecs_cluster_name = module.application.terrafarming_microservices_ecs_cluster_name
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn

#   terrafarming_microservices_ecs_cluster_id = module.application.terrafarming_microservices_ecs_cluster_id
# }

# module "image_analysis_lambda" {
#   source = "./modules/services/lambdas/image-analysis"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   // microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   // microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   general_public_sg_id           = module.compute.general_public_sg_id

#   iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn
# }

# module "weather_recommendations_lambda" {
#   source = "./modules/services/lambdas/weather-recommendation"

#   aws_region                  = var.aws_region
#   vpc_id                      = module.network.vpc_id
#   private_subnet_id1          = module.network.private_subnet_ids[0]
#   private_subnet_id2          = module.network.private_subnet_ids[1]
#   // microservices_load_balancer_arn           = module.compute.microservices_load_balancer_arn
#   // microservices_load_balancer_dns_name      = module.compute.microservices_load_balancer_dns_name
#   ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
# #   general_public_sg_id           = module.compute.general_public_sg_id

#   iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
#   cloudwatch_event_bus_name = module.integration.cloudwatch_event_bus_name

#   sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
# }

# module "mobile" {
#   source = "./modules/services/mobile"

#   amplify_mobile_service_role_arn = module.identity_compliance.amplify_mobile_service_role_arn
# }

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

  terrafarming_website_ecs_cluster_id               = module.application.terrafarming_website_ecs_cluster_id
  terrafarming_website_ecs_cluster_name             = module.application.terrafarming_website_ecs_cluster_name
  website_sg_id                                     = module.compute.website_sg_id
  cloudwatch_log_group_website_container_name       = module.management_governance.cloudwatch_log_group_website_container_name
  cloudwatch_log_group_website_task_definition_name = module.management_governance.cloudwatch_log_group_website_task_definition_name
}

# module "delivery-application" {
#   source = "./modules/delivery-application"

#   uri_invoke_arn_lambda_function = module.compute.invoke_arn_lambda_function
# }

# module "AI-analytics" {
#   source = "./modules/AI-analytics"
# }