variable "bastion_host_ssh_cidr_block" {
    type        = string
    description = "IP address range for devices that can SSH into the bastion host"
    default = "0.0.0.0/0"
}

variable "private_subnet_web_server_cidr_block" {
    type        = string
    description = "IP address range for the private web server subnet in the VPC"
    default     = "10.0.3.0/24"
}

variable "public_subnet_app_cidr_block" {
    type        = string
    description = "IP address range for the public app entry point subnet in the VPC"
    default     = "10.0.1.0/24" 
}

variable "public_subnet_nat_cidr_block" {
    type        = string
    description = "IP address range for the public NAT Gateway subnet in the VPC"
    default     = "10.0.0.0/24"
}

variable "vpc_cidr_block" {
    type        = string
    description = "IP address range in the VPC"
    default     = "10.0.0.0/16"
}