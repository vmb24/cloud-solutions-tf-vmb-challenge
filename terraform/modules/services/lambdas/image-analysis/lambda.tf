# resource "aws_lambda_function" "llm_fruit_image_processing" {
#   function_name = "llm-fruit-image-processing"
#   role          = var.iam_role_lambda_exec_arn
#   package_type  = "Image"
#   image_uri     = "${aws_ecr_repository.fruit_image_processing.repository_url}:latest"
#   timeout       = 300

#   environment {
#     variables = {
#       TABLE_NAME = "PlantHealth"
#     }
#   }

#   lifecycle {
#     ignore_changes = [image_uri]  # Ignora mudanças no URI da imagem para evitar recriação
#   }
# }
