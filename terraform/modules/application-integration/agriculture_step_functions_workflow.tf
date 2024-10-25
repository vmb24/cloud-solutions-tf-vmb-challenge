resource "aws_sfn_state_machine" "agriculture_workflow" {
  name     = "AgricultureWorkflow"
  role_arn = var.step_function_role_arn

  definition = jsonencode({
    Comment = "Agriculture Data Processing, Recommendations, Task Planning, Content Generation, and Accessibility Workflow"
    StartAt = "ProcessSensorsData"
    States = {
      ProcessSensorsData = {
        Type = "Parallel"
        Branches = [
          {
            StartAt = "ProcessSoilMoisture"
            States = {
              ProcessSoilMoisture = {
                Type     = "Task"
                Resource = var.soil_moisture_data_processing_recommendations_lambda_arn
                Next     = "SoilMoistureTaskPlanner"
              }
              SoilMoistureTaskPlanner = {
                Type     = "Task"
                Resource = var.soil_moisture_task_planner_lambda_arn
                Next     = "GenerateSoilMoistureContent"
              }
              GenerateSoilMoistureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateSoilMoistureGifs"
                    States = {
                      GenerateSoilMoistureGifs = {
                        Type     = "Task"
                        Resource = var.generate_gifs_to_soil_moisture_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilMoistureImage"
                    States = {
                      GenerateSoilMoistureImage = {
                        Type     = "Task"
                        Resource = var.generate_images_to_soil_moisture_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessSoilTemperature"
            States = {
              ProcessSoilTemperature = {
                Type     = "Task"
                Resource = var.soil_temperature_data_processing_recommendations_lambda_arn
                Next     = "SoilTemperatureTaskPlanner"
              }
              SoilTemperatureTaskPlanner = {
                Type     = "Task"
                Resource = var.soil_temperature_task_planner_lambda_arn
                Next     = "GenerateSoilTemperatureContent"
              }
              GenerateSoilTemperatureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateSoilTemperatureGifs"
                    States = {
                      GenerateSoilTemperatureGifs = {
                        Type     = "Task"
                        Resource = var.generate_gifs_to_soil_temperature_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateSoilTemperatureImage"
                    States = {
                      GenerateSoilTemperatureImage = {
                        Type     = "Task"
                        Resource = var.generate_images_to_soil_temperature_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessAirMoisture"
            States = {
              ProcessAirMoisture = {
                Type     = "Task"
                Resource = var.air_moisture_data_processing_recommendations_lambda_arn
                Next     = "AirMoistureTaskPlanner"
              }
              AirMoistureTaskPlanner = {
                Type     = "Task"
                Resource = var.air_moisture_task_planner_lambda_arn
                Next     = "GenerateAirMoistureContent"
              }
              GenerateAirMoistureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateAirMoistureGifs"
                    States = {
                      GenerateAirMoistureGifs = {
                        Type     = "Task"
                        Resource = var.generate_gifs_to_air_moisture_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirMoistureImage"
                    States = {
                      GenerateAirMoistureImage = {
                        Type     = "Task"
                        Resource = var.generate_images_to_air_moisture_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessAirTemperature"
            States = {
              ProcessAirTemperature = {
                Type     = "Task"
                Resource = var.air_temperature_data_processing_recommendations_lambda_arn
                Next     = "AirTemperatureTaskPlanner"
              }
              AirTemperatureTaskPlanner = {
                Type     = "Task"
                Resource = var.air_temperature_task_planner_lambda_arn
                Next     = "GenerateAirTemperatureContent"
              }
              GenerateAirTemperatureContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateAirTemperatureGifs"
                    States = {
                      GenerateAirTemperatureGifs = {
                        Type     = "Task"
                        Resource = var.generate_gifs_to_air_temperature_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateAirTemperatureImage"
                    States = {
                      GenerateAirTemperatureImage = {
                        Type     = "Task"
                        Resource = var.generate_images_to_air_temperature_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                ]
                End = true
              }
            }
          },
          {
            StartAt = "ProcessBrightness"
            States = {
              ProcessBrightness = {
                Type     = "Task"
                Resource = var.brightness_processing_recommendations_lambda_arn
                Next     = "BrightnessTaskPlanner"
              }
              BrightnessTaskPlanner = {
                Type     = "Task"
                Resource = var.brightness_task_planner_lambda_arn
                Next     = "GenerateBrightnessContent"
              }
              GenerateBrightnessContent = {
                Type = "Parallel"
                Branches = [
                  {
                    StartAt = "GenerateBrightnessGifs"
                    States = {
                      GenerateBrightnessGifs = {
                        Type     = "Task"
                        Resource = var.generate_gifs_to_brightness_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                  {
                    StartAt = "GenerateBrightnessImage"
                    States = {
                      GenerateBrightnessImage = {
                        Type     = "Task"
                        Resource = var.generate_images_to_brightness_metric_lambda_arn
                        End      = true
                      }
                    }
                  },
                ]
                End = true
              }
            }
          },
        ]
        End = true  # Finaliza o Step Function geral aqui
      },
    }
  })
}
