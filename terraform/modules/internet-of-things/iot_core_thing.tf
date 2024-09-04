resource "aws_iot_thing" "moisture_sensor" {
  name = "moisture_sensor"
}

resource "null_resource" "iot_initialize_shadow" {
  depends_on = [aws_iot_thing.moisture_sensor]

  provisioner "local-exec" {
    command = <<EOF
aws iot-data update-thing-shadow \
  --thing-name moisture_sensor \
  --cli-binary-format raw-in-base64-out \
  --payload '{"state":{"reported":{"moisture":0,"status":"ok"}}}' \
  shadow-output.json
EOF
  }
}