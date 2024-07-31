## Cache Policy
resource "aws_cloudfront_cache_policy" "production" {
  name        = "custom-cache-policy"
  default_ttl = 180
  max_ttl     = 300
  min_ttl     = 1
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = ["Host", "Origin", "Referer", "CUSTOM-HEADER"]
      }
    }
    query_strings_config {
      query_string_behavior = "none"
    }
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }
}

## Origin Request Policy
resource "aws_cloudfront_origin_request_policy" "production" {
  name = "custom-origin-request-policy"
  cookies_config {
    cookie_behavior = "none"
  }
  headers_config {
    header_behavior = "whitelist"
    headers {
      items = ["Host", "Origin", "Referer", "CUSTOM-HEADER"]
    }
  }
  query_strings_config {
    query_string_behavior = "none"
  }
}

resource "aws_cloudfront_distribution" "terrafarming_distribution" {
  enabled         = true
  # is_ipv6_enabled = true
  aliases = ["terrafarming.com.br"]
  price_class = "PriceClass_200"  # Inclui a América do Sul e outros locais

  origin {
    domain_name = var.website_load_balancer_dns_name
    origin_id   = var.website_lb_id
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "match-viewer"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
    origin_shield {
      enabled              = false
      origin_shield_region = var.aws_region
    }
  }

  logging_config {
    bucket          = "${var.cloudfront_logging_bucket_regional_domain_name}"
    include_cookies = false
    prefix          = "cloudfront-logs/"
  }

  default_cache_behavior {
    allowed_methods          = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods           = ["GET", "HEAD"]
    target_origin_id         = var.website_lb_id
    compress                 = true
    viewer_protocol_policy   = "redirect-to-https"
    origin_request_policy_id = aws_cloudfront_origin_request_policy.production.id
    cache_policy_id          = aws_cloudfront_cache_policy.production.id
    min_ttl                  = 0
    max_ttl                  = 0
    default_ttl              = 0
    # Remover forwarded_values
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["BR", "US", "CA", "GB", "DE"]
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.cert.arn
    ssl_support_method  = "sni-only"
  }

  tags = {
    Name = "terrafarming-cloudfront-distribution"
  }
}
