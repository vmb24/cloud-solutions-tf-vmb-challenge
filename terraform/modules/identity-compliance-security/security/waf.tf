resource "aws_wafv2_web_acl" "app_waf" {
  name        = "agricultural-app-waf"
  description = "WAF for agricultural application"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "AgriculturalAppWAFMetrics"
    sampled_requests_enabled   = true
  }

  # Adicione regras conforme necessário
}