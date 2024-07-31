# output "cloudfront_oai_id" {
#   value = aws_cloudfront_origin_access_identity.my_oai.id
# }

output "acm_certificate_cert_arn" {
  value = aws_acm_certificate.cert.arn
}

output "route53_record_www_record_name" {
  value = aws_route53_record.www_record.name
}