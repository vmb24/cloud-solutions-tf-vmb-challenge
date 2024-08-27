# Kinesis Video Stream
resource "aws_kinesis_video_stream" "task_planner_video_stream" {
  name                    = "task_planner_video_stream"
  data_retention_in_hours = 24
  device_name             = "task_planner_device"
}