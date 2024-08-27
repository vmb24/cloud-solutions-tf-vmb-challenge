resource "aws_iot_thing" "parking_sensor" {
  name = "parking_sensor"
}

resource "null_resource" "iot_initialize_shadow" {
  depends_on = [aws_iot_thing.parking_sensor]

  provisioner "local-exec" {
    command = <<EOF
aws iot-data update-thing-shadow \
  --thing-name parking_sensor \
  --cli-binary-format raw-in-base64-out \
  --payload '{"state":{"reported":{"distance": 100.0, "status": "disponível"}}}' \
  shadow-output.json
EOF
  }
}