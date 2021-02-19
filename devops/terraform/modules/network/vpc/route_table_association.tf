resource "aws_route_table_association" "private_subnet_web_server_rt_assoc" {
    subnet_id      = aws_subnet.private_subnet_web_server.id
    route_table_id = aws_route_table.private_subnet_web_server_rt.id 
}

resource "aws_route_table_association" "public_subnet_app_rt_assoc" {
    subnet_id      = aws_subnet.public_subnet_app.id
    route_table_id = aws_route_table.public_subnet_app_rt.id 
}

resource "aws_route_table_association" "public_subnet_nat_rt_assoc" {
    subnet_id      = aws_subnet.public_subnet_nat.id
    route_table_id = aws_route_table.public_subnet_nat_rt.id
}