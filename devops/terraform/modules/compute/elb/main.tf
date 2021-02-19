resource "aws_autoscaling_attachment" "asg_attachment" {
    autoscaling_group_name = aws_autoscaling_group.scale_app.id
    elb                    = aws_elb.app_elb.id
}

resource "aws_elb" "app_elb" {
    name = "vocab-manager-app-elb"
    subnets = [var.public_subnet_id]

    listener {
        instance_port     = 5000
        instance_protocol = "http"
        lb_port           = 80
        lb_protocol       = "http"
    }
}