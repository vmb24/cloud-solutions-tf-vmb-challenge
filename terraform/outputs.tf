output "certificate_pem" {
  value = module.internet_of_things.certificate_pem
  sensitive = true
}

output "public_key" {
  value = module.internet_of_things.public_key
  sensitive = true
}

output "private_key" {
  value = module.internet_of_things.private_key
  sensitive = true
}

output "iot_endpoint" {
  value = module.internet_of_things.iot_endpoint
}