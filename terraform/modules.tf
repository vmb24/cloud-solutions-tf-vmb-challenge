module "identity-compliance" {
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

  vpc_id                           = module.network.vpc_id
  subnet_id1                       = module.network.private_subnet_ids[0]
  subnet_id2                       = module.network.private_subnet_ids[1]
  ecs_task_execution_role          = module.identity-compliance.ecs_task_execution_role_arn
  llm_soil_metrics_repository_name = var.llm_soil_metrics_repository_name
}
