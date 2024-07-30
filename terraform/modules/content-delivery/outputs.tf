# output "cloudfront_oai_id" {
#   value = aws_cloudfront_origin_access_identity.my_oai.id
# }

output "acm_certificate_cert_arn" {
  value = aws_acm_certificate.cert.arn
}