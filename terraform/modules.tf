module "identity_compliance" {
  source = "./modules/identity-compliance"
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

  aws_region                       = var.aws_region
  vpc_id                           = module.network.vpc_id
  public_subnet_id1                = module.network.public_subnet_ids[0]
  public_subnet_id2                = module.network.public_subnet_ids[1]
  private_subnet_id1               = module.network.private_subnet_ids[0]
  private_subnet_id2               = module.network.private_subnet_ids[1]
}

module "farmer_service" {
  source = "./modules/services/microservices/farmer-service"

  aws_region                  = var.aws_region
  vpc_id                      = module.network.vpc_id
  private_subnet_id1          = module.network.private_subnet_ids[0]
  private_subnet_id2          = module.network.private_subnet_ids[1]
  load_balancer_arn           = module.compute.load_balancer_arn
  ecs_task_execution_role_arn = module.identity_compliance.ecs_task_execution_role_arn
  ecs_task_role_arn           = module.identity_compliance.ecs_task_role_arn
  load_balancer_dns_name      = module.compute.load_balancer_dns_name
  ecs_service_sg_id           = module.compute.ecs_service_sg_id
  
  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name
  sns_topic_soil_metrics_notifications_arn = module.soil_metrics_service.sns_topic_soil_metrics_notifications_arn
  sns_topic_weather_notifications_arn = module.weather_service.sns_topic_weather_notifications_arn
}

module "application-services" {
  source = "./modules/application-services"
}

module "storage" {
  source = "./modules/storage"

  bucket_name = var.bucket_name
  environment = var.environment
}

module "database" {
  source = "./modules/database"
}

module "soil_metrics_service" {
  source = "./modules/services/microservices/soil-metrics-service"

  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn
  sns_topic_equipment_health_notifications_arn = module.equipment_health_service.sns_topic_equipment_health_notifications_arn
}

module "crop_health_service" {
  source = "./modules/services/microservices/crop-health-service"

  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
  sns_topic_greenhouse_notifications_arn = module.greenhouse_service.sns_topic_greenhouse_notifications_arn
}

module "equipment_health_service" {
  source = "./modules/services/microservices/equipment-health-service"

  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name
  sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
  sns_topic_soil_metrics_notifications_arn = module.soil_metrics_service.sns_topic_soil_metrics_notifications_arn
}

module "weather_service" {
  source = "./modules/services/microservices/weather-service"

  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_weather_recommendation_notifications_arn = module.weather_recommendations_lambda.sns_topic_weather_recommendation_notifications_arn
  sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn
}

module "greenhouse_service" {
  source = "./modules/services/microservices/greenhouse-service"

  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
}

module "image_analysis_lambda" {
  source = "./modules/services/lambdas/image-analysis"

  iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_crop_health_notifications_arn = module.crop_health_service.sns_topic_crop_health_notifications_arn
}

module "weather_recommendations_lambda" {
  source = "./modules/services/lambdas/weather-recommendation"

  iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
  cloudwatch_event_bus_name = module.application-services.cloudwatch_event_bus_name

  sns_topic_farmer_notifications_arn = module.farmer_service.sns_topic_farmer_notifications_arn
}

module "mobile" {
  source = "./modules/mobile"

  amplify_mobile_service_role_arn = module.identity_compliance.amplify_mobile_service_role_arn
}

# module "delivery-application-services" {
#   source = "./modules/delivery-application-services"

#   uri_invoke_arn_lambda_function = module.compute.invoke_arn_lambda_function
# }

# module "AI-analytics" {
#   source = "./modules/AI-analytics"
# }