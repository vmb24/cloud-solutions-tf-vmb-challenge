variable "vpc_cidr" {
    type = string
}

variable "availability_zones" {
    type = list(string)
}

variable "private_subnet_cidrs" {
    type = list(string)
}

variable "public_subnet_cidrs" {
    type = list(string)
}