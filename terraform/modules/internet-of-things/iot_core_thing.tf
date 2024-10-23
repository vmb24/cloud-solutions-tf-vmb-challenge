resource "aws_iot_thing" "agricultural_sensor" {
  name = "agricultural_sensor"

  attributes = {
    sensor_type = "agricultural"
    location    = "field_1_terrafarming"  # Você pode ajustar isso conforme necessário
  }
}

resource "aws_iot_thing_type" "agricultural_sensor_type" {
  name = "agricultural_sensor_type"

  properties {
    description = "Sensor type for agricultural monitoring"
    searchable_attributes = ["sensor_type", "location"]
  }
}

resource "null_resource" "iot_initialize_shadow_terrafarming" {
  depends_on = [aws_iot_thing.agricultural_sensor]

  provisioner "local-exec" {
    command = <<EOF
aws iot-data update-thing-shadow \
  --thing-name agricultural_sensor \
  --cli-binary-format raw-in-base64-out \
  --payload '{
    "state": {
      "reported": {
        "soilMoisture": {
          "value": 0,
          "status": "Unknown",
          "crops": ["Cultura 1", "Cultura 2"]
        },
        "soilTemperature": {
          "value": 0,
          "status": "Unknown",
          "crops": ["Cultura 1", "Cultura 2"]
        },
        "airMoisture": {
          "value": 0,
          "status": "Unknown",
          "crops": ["Cultura 1", "Cultura 2"]
        },
        "airTemperature": {
          "value": 0,
          "status": "Unknown",
          "crops": ["Cultura 1", "Cultura 2"]
        },
        "brightness": {
          "digital": 0,
          "analog": 0,
          "status": "Unknown",
          "crops": ["Cultura 1", "Cultura 2"]
        }
      }
    }
  }' \
  shadow-output.json
EOF
  }
}