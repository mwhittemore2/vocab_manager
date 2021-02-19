resource "aws_network_acl" "app_acl" {
    vpc_id     = aws_vpc.main.id
    subnet_ids = [aws_subnet.public_subnet_app.id]
}