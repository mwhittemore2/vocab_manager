resource "aws_security_group" "connect_bastion_host" {
    name   = "connect_bastion_host"
    vpc_id = aws_vpc.main.id

    ingress {
        description = "Ping bastion host to test connectivity"
        from_port   = -1
        to_port     = -1
        protocol    = "icmp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "SSH into bastion host"
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [var.bastion_host_ssh_cidr_block]
    }
}

resource "aws_security_group" "ssh_private_instance" {
    name   = "ssh_private_instance"
    vpc_id = aws_vpc.main.id

    ingress {
        description     = "SSH from bastion host to private instance"
        from_port       = 22
        to_port         = 22
        protocol        = "tcp"
        security_groups = [aws_security_group.connect_bastion_host.id]
    }
}