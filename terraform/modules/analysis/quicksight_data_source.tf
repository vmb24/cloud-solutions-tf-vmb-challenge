# data "aws_caller_identity" "quicksight_data_source_current_caller_identity" {}

# resource "aws_quicksight_data_source" "athena_source" {
#   data_source_id = "athena-agricultural-data"
#   name           = "Agricultural Data (Athena)"
#   type           = "ATHENA"
  
#   aws_account_id = data.aws_caller_identity.quicksight_data_source_current_caller_identity.account_id

#   parameters {
#     athena {
#       work_group = "primary"
#     }
#   }
# }