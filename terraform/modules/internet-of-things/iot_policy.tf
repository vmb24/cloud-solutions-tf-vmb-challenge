resource "aws_iot_policy" "arduino_policy" {
  name   = "ArduinoPolicy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "iot:Connect",
          "iot:Publish",
          "iot:Subscribe",
          "iot:Receive"
        ],
        "Resource": "*"
      }
    ]
  })
}

resource "aws_iot_policy_attachment" "policy_attach" {
  policy =  aws_iot_policy.arduino_policy.name
  target      = aws_iot_certificate.arduino_cert.arn
}

resource "aws_iot_thing_principal_attachment" "thing_attach" {
  thing     = aws_iot_thing.moisture_sensor.name
  principal = aws_iot_certificate.arduino_cert.arn
}