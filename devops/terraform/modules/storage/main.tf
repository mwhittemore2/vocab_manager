provider "aws" {
    region = var.provider_region
}

module "create_s3_buckets" {
    source = "./s3"
}