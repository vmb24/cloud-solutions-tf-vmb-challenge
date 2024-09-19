resource "aws_security_group" "efs_sg" {
  name        = "efs-security-group"
  description = "Security group for EFS mount targets"
  vpc_id      = var.vpc_id  # Certifique-se de que esta variável está definida com o ID da sua VPC

  # Regra de entrada para permitir tráfego NFS da sua VPC
  ingress {
    description     = "NFS from VPC"
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    cidr_blocks     = [var.vpc_cidr_block]  # Use o bloco CIDR da sua VPC
  }

  # Regra de entrada para permitir tráfego NFS dos security groups das tasks do ECS
  ingress {
    description     = "NFS from ECS tasks"
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [aws_security_group.website_sg.id]  # ID do security group das tasks do ECS
  }

  # Regra de saída para permitir todo o tráfego de saída
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "efs-security-group"
  }
}

resource "aws_security_group_rule" "ecs_to_efs" {
  type                     = "egress"
  from_port                = 2049
  to_port                  = 2049
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.efs_sg.id
  security_group_id        = aws_security_group.website_sg.id
}