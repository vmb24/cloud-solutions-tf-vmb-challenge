resource "aws_sfn_state_machine" "agriculture_workflow" {
  name     = "AgricultureWorkflow"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    StartAt = "GenerateAccessibleContent"
    States = {
      GenerateAccessibleContent = {
        Type     = "Task"
        Resource = aws_lambda_function.generate_accessible_content.arn
        Next     = "VideoProcessing"
      }
      VideoGeneration = {
        Type     = "Task"
        Resource = aws_lambda_function.video_generation.arn
        Next     = "VideoGeneration"
      }
      ImageGeneration = {
        Type     = "Task"
        Resource = aws_lambda_function.image_generation.arn
        Next     = "ProcessingMoistureRecommendations"
      }
      ProcessingMoistureRecommendations = {
        Type     = "Task"
        Resource = aws_lambda_function.processing_moisture_recommendations.arn
        Next     = "MoistureTaskPlanner"
      }
      MoistureTaskPlanner = {
        Type     = "Task"
        Resource = aws_lambda_function.moisture_task_planner.arn
        Next     = "MoistureTaskPlanner"
      }
      ImageGeneration = {
        Type     = "Task"
        Resource = aws_lambda_function.image_generation.arn
        End      = true
      }
    }
  })
}