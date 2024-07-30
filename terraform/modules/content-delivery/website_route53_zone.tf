# Configuração da Zona DNS
resource "aws_route53_zone" "terrafarming_zone" {
  name = "terrafarming.com.br"
}