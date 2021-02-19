variable "bastion_host_key_name" {
    type        = string
    description = "The name of the key that allows SSH access to the bastion host"
    default     = ""
}

variable "bastion_host_security_group" {
    type        = string
    description = "The security group to which the bastion host is assigned"
    default     = ""
}

variable "deployment" {
    type        = string
    description = "The environment being deployed to"
    default     = "dev"
}

variable "image_spec" {
    type        = string
    description = "The AMI image for the instance"
    default     = ""
}

variable "instance_spec" {
    type        = string
    description = "The type of AWS instance to deploy"
    default     = ""
}

variable "private_subnet_id" {
    type        = string
    description = "The id of the private subnet in the VPC containing the autoscaled web server instances"
    default     = ""
}

variable "project_name" {
    type        = string
    description = "The name of the project being deployed"
    default     = "vocabulary_manager"
}

variable "public_subnet_id" {
    type        = string
    description = "The id of the public subnet in the VPC containing the elb"
    default     = ""
}

variable "web_server_key_name" {
    type        = string
    description = "The name of the key that allows SSH access to a web server"
    default     = ""
}