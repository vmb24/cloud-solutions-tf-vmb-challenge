# Certificado SSL
resource "aws_acm_certificate" "cert" {
  domain_name               = "terrafarming.com.br"
  validation_method         = "DNS"

  subject_alternative_names = [
    "www.terrafarming.com.br",
  ]

  tags = {
    Name = "terrafarming-certificate"
  }
}