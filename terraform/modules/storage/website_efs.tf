resource "aws_efs_file_system" "website_efs" {
  creation_token = "website-efs"
  encrypted      = true

  tags = {
    Name = "website-efs"
  }
}

resource "aws_efs_mount_target" "website_efs_mount" {
  file_system_id = aws_efs_file_system.website_efs.id
  subnet_id      = var.public_subnet_id1
  security_groups = [var.efs_security_group_id]
}