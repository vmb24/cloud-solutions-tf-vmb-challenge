resource "null_resource" "iot_initialize_shadow" {
  depends_on = [aws_iot_thing.agricultural_sensor]

  provisioner "local-exec" {
    command = <<EOF
aws iot-data update-thing-shadow \
  --thing-name agricultural_sensor \
  --cli-binary-format raw-in-base64-out \
  --payload '{"state":{"reported":{"soilMoisture":{"value":0,"status":"Unknown"},"soilTemperature":{"value":0,"status":"Unknown"},"airHumidity":{"value":0,"status":"Unknown"},"airTemperature":{"value":0,"status":"Unknown"},"light":{"digital":0,"analog":0,"status":"Unknown"}}}}' \
  shadow-output.json
EOF
  }
}