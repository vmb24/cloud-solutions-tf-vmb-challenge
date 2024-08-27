resource "aws_cloudfront_distribution" "tech4parking_distribution" {
  enabled         = true
  # is_ipv6_enabled = true
  aliases = ["tech4parking.com.br"]
  price_class     = "PriceClass_All"  # Adjust based on your needs

  origin {
    domain_name = var.website_load_balancer_dns_name
    origin_id   = "website-lb-origin"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    origin_shield {
      enabled = true
      origin_shield_region = "us-east-1"
    }
  }

  # origin_group {
  #   origin_id = "website-lb-origin"
  #   failover_criteria {
  #     status_codes = [400, 403, 404, 416, 500, 502,503,504]
  #   }

  #   member {
  #     origin_id = "website-lb-origin"
  #   }

  #   member {
  #     origin_id = "website-lb2-origin"
  #   }
  # }

  ordered_cache_behavior {
    path_pattern           = "/static/*"
    target_origin_id = "website-lb-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
  }

  default_cache_behavior {
    target_origin_id = "website-lb-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true
    min_ttl         = 0
    max_ttl         = 86400
    default_ttl     = 3600

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
  }

  custom_error_response {
    error_code = 404
    response_code = 404
    response_page_path = "/errors/404.html"
  }

  custom_error_response {
    error_code         = 403
    response_code      = 403
    response_page_path = "/errors/403.html"
  }

  logging_config {
    bucket          = "${var.cloudfront_logging_bucket_regional_domain_name}"
    include_cookies = false
    prefix          = "cloudfront-logs/"
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.cert.arn
    ssl_support_method  = "sni-only"
    minimum_protocol_version = "TLSv1.1_2016"
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["BR", "US", "CA", "GB", "DE"]
    }
  }

  tags = {
    Name = "tech4parking-cloudfront-distribution"
  }
}