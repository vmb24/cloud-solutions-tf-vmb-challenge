module "identity-compliance" {
    source = "./modules/identity-compliance"
}

module "network" {
    source = "./modules/network"

    vpc_cidr = var.vpc_cidr
    availability_zones = var.availability_zones
    private_subnet_cidrs = var.private_subnet_cidrs
    public_subnet_cidrs = var.public_subnet_cidrs
}  

module "compute" {
  source = "./modules/compute"

  vpc_id = module.network.vpc_id
}