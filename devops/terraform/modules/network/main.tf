provider "aws" {
    region = var.provider_region
}

module "setup_vpc" {
    source = "./vpc"
}