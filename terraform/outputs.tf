output "certificate_pem" {
  value     = module.internet_of_things.certificate_pem
  sensitive = true
}

output "public_key" {
  value     = module.internet_of_things.public_key
  sensitive = true
}

output "private_key" {
  value     = module.internet_of_things.private_key
  sensitive = true
}

output "iot_endpoint" {
  value = module.internet_of_things.iot_endpoint
}

output "parking_spot_management_api_url" {
  value = module.parking_spot_management.parking_spot_management_api_url
}

output "parking_spot_status_update_api_url" {
  value = module.parking_spot_status_update.parking_spot_status_update_api_url
}