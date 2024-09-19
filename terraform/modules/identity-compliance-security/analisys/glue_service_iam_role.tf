data "aws_caller_identity" "glue_service_current_caller_identity" {}

resource "aws_iam_role" "glue_role" {
  name = "AWSGlueServiceRoleForDynamoDB"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "dynamodb_access" {
  name = "DynamoDBAccessForGlue"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:DescribeTable",
          "dynamodb:Scan",
          "dynamodb:GetItem",
          "dynamodb:GetRecords"
        ]
        Resource = "arn:aws:dynamodb:*:${data.aws_caller_identity.glue_service_current_caller_identity.account_id}:table/*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "s3_access" {
  name = "S3AccessForGlue"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::aws-glue-*",
          "arn:aws:s3:::aws-glue-*/*"
        ]
      }
    ]
  })
}