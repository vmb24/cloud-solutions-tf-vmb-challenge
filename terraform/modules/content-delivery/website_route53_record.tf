resource "aws_route53_record" "terrafarming_record" {
  zone_id = aws_route53_zone.terrafarming_zone.id
  name    = "terrafarming.com.br"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.terrafarming_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.terrafarming_distribution.hosted_zone_id
    evaluate_target_health = true
  }
}
