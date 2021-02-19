resource "aws_subnet" "private_subnet_web_server" {
    vpc_id     = aws_vpc.main.id
    cidr_block = var.private_subnet_web_server_cidr_block 
}

resource "aws_subnet" "public_subnet_app" {
    vpc_id     = aws_vpc.main.id
    cidr_block = var.public_subnet_app_cidr_block
}

resource "aws_subnet" "public_subnet_nat" {
    vpc_id     = aws_vpc.main.id
    cidr_block = var.public_subnet_nat_cidr_block
}