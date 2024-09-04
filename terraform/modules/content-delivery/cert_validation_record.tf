# Registros de Validação
resource "aws_route53_record" "cert_validation_record" {
  for_each = { for opt in aws_acm_certificate.cert.domain_validation_options : opt.domain_name => opt }

  zone_id = aws_route53_zone.terrafarming_zone.id
  name    = each.value.resource_record_name
  type    = each.value.resource_record_type
  ttl     = 60
  records = [each.value.resource_record_value]

  # alias {
  #   name                   = var.website_load_balancer_dns_name
  #   zone_id                = var.website_lb_zone_id
  #   evaluate_target_health = true
  # }
}