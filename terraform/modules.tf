module "internet_of_things" {
  source = "./modules/internet-of-things"

  aws_region                            = var.aws_region
  parking_spot_management_lambda_arn    = module.parking_spot_management.parking_spot_management_lambda_arn
  parking_spot_status_update_lambda_arn = module.parking_spot_status_update.parking_spot_status_update_lambda_arn
}

module "identity_compliance_security" {
  source = "./modules/identity-compliance-security"

  aws_region                       = var.aws_region
  ecs_website_service_name         = var.ecs_website_service_name
  dynamodb_table_parking_spots_arn = module.database.dynamodb_table_parking_spots_arn
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
  // private_subnet_id1 = module.network.private_subnet_ids[0]
  // private_subnet_id2 = module.network.private_subnet_ids[1]
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

module "storage" {
  source = "./modules/storage"

  bucket_name = var.bucket_name
  environment = var.environment

  moisture_task_planner_lambda_arn = module.moisture_task_planner.moisture_task_planner_lambda_arn
  allow_s3_moisture_task_planner   = module.moisture_task_planner.allow_s3_moisture_task_planner
}

module "database" {
  source = "./modules/database"
}

module "parking_spot_management" {
  source = "./modules/services/lambda/parking-spot-management"

  parking_spot_management_lambda_role_arn = module.identity_compliance_security.parking_spot_management_lambda_role_arn
  parking_spot_iot_rule_arn               = module.internet_of_things.parking_spot_iot_rule_arn
}

module "parking_spot_status_update" {
  source = "./modules/services/lambda/parking-spot-status-update"

  parking_spot_status_update_lambda_role_arn = module.identity_compliance_security.parking_spot_status_update_lambda_role_arn
  parking_spot_iot_rule_arn                  = module.internet_of_things.parking_spot_iot_rule_arn
}

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
  acm_certificate_cert_arn       = var.http_certificate
  route53_record_www_record_name = var.route53_record_www_record_name

  tech4parking_website_ecs_cluster_id               = module.application.tech4parking_website_ecs_cluster_id
  tech4parking_website_ecs_cluster_name             = module.application.tech4parking_website_ecs_cluster_name
  website_sg_id                                     = module.compute.website_sg_id
  cloudwatch_log_group_website_container_name       = module.management_governance.cloudwatch_log_group_website_container_name
  cloudwatch_log_group_website_task_definition_name = module.management_governance.cloudwatch_log_group_website_task_definition_name
}

module "analyse" {
  source = "./modules/analyse"
}

/*
module "machine_learning" {
  source = "./modules/machine-learning"
} */