# Certificado SSL
resource "aws_acm_certificate" "cert" {
  domain_name               = "tech4parking.com.br"
  validation_method         = "DNS"

  subject_alternative_names = [
    "www.tech4parking.com.br",
  ]

  tags = {
    Name = "tech4parking-certificate"
  }
}
