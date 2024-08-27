# Configuração da Zona DNS
resource "aws_route53_zone" "tech4parking_zone" {
  name = "tech4parking.com.br"
}