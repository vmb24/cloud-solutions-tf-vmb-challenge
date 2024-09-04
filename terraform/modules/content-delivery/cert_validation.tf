# Validação do Certificado ACM
resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn = aws_acm_certificate.cert.arn

  validation_record_fqdns = [
    for r in aws_route53_record.cert_validation_record : r.fqdn
  ]
}