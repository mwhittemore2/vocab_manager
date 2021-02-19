resource "aws_autoscaling_group" "scale_app" {
    name = "vocab_manager_auto_scale"
    max_size = 1
    min_size = 1
    launch_template {
        id      = aws_launch_template.web_server.id
        version = aws_launch_template.web_server.latest_version
    }

    tag {
        key                 = "Name"
        value               = join(".", [var.project_name, var.deployment, "scale_web_server", "autoscaling_group"])
        propagate_at_launch = false
    }
}