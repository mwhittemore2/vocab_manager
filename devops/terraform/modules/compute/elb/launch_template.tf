resource "aws_launch_template" "web_server" {
    name               = "vocab_manager_web_server"
    image_id           = var.image_spec
    instance_type      = var.instance_spec
    key_name           = var.web_server_key_name
    user_data          = file("${path.module}/init_instance.sh")
    
    network_interfaces {
        subnet_id = var.private_subnet_id
    }

    tag_specifications {
        resource_type = "instance"

        tags = {
            Name = join(".", [var.project_name, var.deployment, "web_server", "ec2"])
        }
    }
}