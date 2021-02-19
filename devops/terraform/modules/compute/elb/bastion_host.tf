resource "aws_instance" "bastion_host" {
    ami             = var.image_spec
    instance_type   = var.instance_spec
    key_name        = var.bastion_host_key_name
    security_groups = [var.bastion_host_security_group]
    subnet_id       = var.public_subnet_id

    tags = {
        Name = join(".", [var.project_name, var.deployment, "bastion_host", "ec2"])
    }
}