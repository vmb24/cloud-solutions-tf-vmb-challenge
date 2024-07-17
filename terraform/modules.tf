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
}

module "soil_metrics_service" {
  source = "./modules/services/microservices/soil-metrics-service"
}

module "crop_health_service" {
  source = "./modules/services/microservices/crop-health-service"
}

module "equipment_health_service" {
  source = "./modules/services/microservices/equipment-health-service"
}

module "weather_service" {
  source = "./modules/services/microservices/weather-service"
}

module "greenhouse_service" {
  source = "./modules/services/microservices/greenhouse-service"
}

module "fruit_image_processing_lambda" {
  source = "./modules/services/lambdas/fruit-image-processing"

  iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
}

module "soil_recommendations_lambda" {
  source = "./modules/services/lambdas/soil-recommendations"

  iam_role_lambda_exec_arn = module.identity_compliance.iam_role_lambda_exec_arn
}

# module "application-services" {
#   source = "./modules/application-services"
# }

# module "delivery-application-services" {
#   source = "./modules/delivery-application-services"

#   uri_invoke_arn_lambda_function = module.compute.invoke_arn_lambda_function
# }

# module "AI-analytics" {
#   source = "./modules/AI-analytics"
# }

# module "database" {
#   source = "./modules/database"
# }