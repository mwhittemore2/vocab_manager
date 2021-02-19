provider "aws" {
    region = var.provider_region
}

module "elb" {
    source = "./elb"
}