resource "aws_iot_thing" "agricultural_sensor" {
  name = "agricultural_sensor"

  attributes = {
    sensor_type = "agricultural"
    location    = "field_1"  # Você pode ajustar isso conforme necessário
  }
}

resource "aws_iot_thing_type" "agricultural_sensor_type" {
  name = "agricultural_sensor_type"

  properties {
    description = "Sensor type for agricultural monitoring"
    searchable_attributes = ["sensor_type", "location"]
  }
}

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