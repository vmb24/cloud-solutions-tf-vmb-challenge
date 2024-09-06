resource "aws_sfn_state_machine" "agriculture_workflow" {
  name     = "AgricultureWorkflow"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "Agriculture Data Processing, Recommendations, Task Planning, and Content Generation Workflow"
    StartAt = "ProcessSensorsData"
    States = {
      ProcessSensorsData = {
        Type = "Parallel"
        Branches = [
          {
            StartAt = "ProcessSoilMoisture"
            States = {
              SoilMoistureDataProcessingRecommendations = {
                Type     = "Task"
                Resource = aws_lambda_function.processing_moisture_recommendations.arn
                Next     = "SoilMoistureTaskPlanner"
              }
              SoilMoistureTaskPlanner = {
                Type     = "Task"
                Resource = aws_lambda_function.moisture_task_planner.arn
                Next     = "GenerateSoilMoistureContent"
              }
              GenerateSoilMoistureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateSoilMoistureVideo"
                    States = {
                      GenerateSoilMoistureVideo = {
                        Type     = "Task"
                        Resource = aws_lambda_function.video_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilMoistureImage"
                    States = {
                      GenerateSoilMoistureImage = {
                        Type     = "Task"
                        Resource = aws_lambda_function.image_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilMoistureAccessibleContent"
                    States = {
                      GenerateSoilMoistureAccessibleContent = {
                        Type     = "Task"
                        Resource = aws_lambda_function.generate_accessible_content.arn
                        End      = true
                      }
                    }
                  }
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessSoilTemperature"
            States = {
              SoilTemperatureDataProcessingRecommendations = {
                Type     = "Task"
                Resource = aws_lambda_function.processing_temperature_recommendations.arn
                Next     = "SoilTemperatureTaskPlanner"
              }
              SoilTemperatureTaskPlanner = {
                Type     = "Task"
                Resource = aws_lambda_function.temperature_task_planner.arn
                Next     = "GenerateSoilTemperatureContent"
              }
              GenerateSoilTemperatureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateSoilTemperatureVideo"
                    States = {
                      GenerateSoilTemperatureVideo = {
                        Type     = "Task"
                        Resource = aws_lambda_function.video_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilTemperatureImage"
                    States = {
                      GenerateSoilTemperatureImage = {
                        Type     = "Task"
                        Resource = aws_lambda_function.image_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilTemperatureAccessibleContent"
                    States = {
                      GenerateSoilTemperatureAccessibleContent = {
                        Type     = "Task"
                        Resource = aws_lambda_function.generate_accessible_content.arn
                        End      = true
                      }
                    }
                  }
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessAirMoisture"
            States = {
              AirMoistureDataProcessingRecommendations = {
                Type     = "Task"
                Resource = aws_lambda_function.processing_moisture_recommendations.arn
                Next     = "AirMoistureTaskPlanner"
              }
              AirMoistureTaskPlanner = {
                Type     = "Task"
                Resource = aws_lambda_function.moisture_task_planner.arn
                Next     = "GenerateAirMoistureContent"
              }
              GenerateAirMoistureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateAirMoistureVideo"
                    States = {
                      GenerateAirMoistureVideo = {
                        Type     = "Task"
                        Resource = aws_lambda_function.video_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirMoistureImage"
                    States = {
                      GenerateAirMoistureImage = {
                        Type     = "Task"
                        Resource = aws_lambda_function.image_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirMoistureAccessibleContent"
                    States = {
                      GenerateAirMoistureAccessibleContent = {
                        Type     = "Task"
                        Resource = aws_lambda_function.generate_accessible_content.arn
                        End      = true
                      }
                    }
                  }
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessAirTemperature"
            States = {
              AirTemperatureDataProcessingRecommendations = {
                Type     = "Task"
                Resource = aws_lambda_function.processing_temperature_recommendations.arn
                Next     = "AirTemperatureTaskPlanner"
              }
              AirTemperatureTaskPlanner = {
                Type     = "Task"
                Resource = aws_lambda_function.temperature_task_planner.arn
                Next     = "GenerateAirTemperatureContent"
              }
              GenerateAirTemperatureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateAirTemperatureVideo"
                    States = {
                      GenerateAirTemperatureVideo = {
                        Type     = "Task"
                        Resource = aws_lambda_function.video_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirTemperatureImage"
                    States = {
                      GenerateAirTemperatureImage = {
                        Type     = "Task"
                        Resource = aws_lambda_function.image_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirTemperatureAccessibleContent"
                    States = {
                      GenerateAirTemperatureAccessibleContent = {
                        Type     = "Task"
                        Resource = aws_lambda_function.generate_accessible_content.arn
                        End      = true
                      }
                    }
                  }
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessLight"
            States = {
              LightDataProcessingRecommendations = {
                Type     = "Task"
                Resource = aws_lambda_function.processing_light_recommendations.arn
                Next     = "LightTaskPlanner"
              }
              LightTaskPlanner = {
                Type     = "Task"
                Resource = aws_lambda_function.light_task_planner.arn
                Next     = "GenerateLightContent"
              }
              GenerateLightContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateLightVideo"
                    States = {
                      GenerateLightVideo = {
                        Type     = "Task"
                        Resource = aws_lambda_function.video_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateLightImage"
                    States = {
                      GenerateLightImage = {
                        Type     = "Task"
                        Resource = aws_lambda_function.image_generation.arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateLightAccessibleContent"
                    States = {
                      GenerateLightAccessibleContent = {
                        Type     = "Task"
                        Resource = aws_lambda_function.generate_accessible_content.arn
                        End      = true
                      }
                    }
                  }
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ManageTasks"
            States = {
              ExecuteTasks = {
                Type     = "Task"
                Resource = aws_lambda_function.task_manager.arn
                End      = true
              }
            }
          }
        ]
        Next = "MergeBranchResults"
      },
      MergeBranchResults = {
        Type     = "Task"
        Resource = aws_lambda_function.tasks_results_merge.arn
        End      = true
      }
    }
  })
}