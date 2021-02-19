resource "aws_network_acl_rule" "receive_client_http_request" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 100
    egress         = false
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = "0.0.0.0/0"
    from_port      = 80
    to_port        = 80
}

#Send load-balanced request to private subnet
resource "aws_network_acl_rule" "forward_private_subnet" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 101
    egress         = false
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = var.public_subnet_app_cidr_block
    from_port      = 1024
    to_port        = 65535
}

resource "aws_network_acl_rule" "receive_private_subnet_response" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 102
    egress         = true
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = var.public_subnet_app_cidr_block
    from_port      = 1024
    to_port        = 65535
}

resource "aws_network_acl_rule" "respond_client_request" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 200
    egress         = true
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = "0.0.0.0/0"
    from_port      = 1024
    to_port        = 65535
}

resource "aws_network_acl_rule" "ssh_into_private_subnet" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 201
    egress         = false
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = var.public_subnet_app_cidr_block
    from_port      = 22
    to_port        = 22
}

resource "aws_network_acl_rule" "ssh_from_internet" {
    network_acl_id = aws_network_acl.app_acl.id
    rule_number    = 202
    egress         = false
    protocol       = "tcp"
    rule_action    = "allow"
    cidr_block     = "0.0.0.0/0"
    from_port      = 22
    to_port        = 22
}