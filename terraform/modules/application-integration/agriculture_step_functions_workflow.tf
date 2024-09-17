resource "aws_sfn_state_machine" "agriculture_workflow" {
  name     = "AgricultureWorkflow"
  role_arn = aws_iam_role.step_function_role.arn

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
                  {
                    StartAt = "GenerateSoilMoistureAccessibleContent"
                    States = {
                      GenerateSoilMoistureAccessibleContent = {
                        Type     = "Task"
                        Resource = var.management_generate_accessible_contents_lambda_arn
                        Next     = "AccessibilityChoice"
                      }
                      AccessibilityChoice = {
                        Type = "Choice"
                        Choices = [
                          {
                            Variable = "$.type"
                            StringEquals = "text_to_speech"
                            Next = "TextToSpeech"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "image_recognition"
                            Next = "ImageRecognition"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "video_caption"
                            Next = "VideoCaption"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "text_simplification"
                            Next = "TextSimplification"
                          }
                        ]
                        Default = "AccessibilityEnd"
                      },
                      TextToSpeech = {
                        Type     = "Task"
                        Resource = var.accessible_text_to_speech_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      ImageRecognition = {
                        Type     = "Task"
                        Resource = var.accessible_image_recognition_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      VideoCaption = {
                        Type     = "Task"
                        Resource = var.accessible_video_caption_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      TextSimplification = {
                        Type     = "Task"
                        Resource = var.accessible_text_simplification_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      AccessibilityEnd = {
                        Type = "Pass"
                        End  = true
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
                  {
                    StartAt = "GenerateSoilTemperatureAccessibleContent"
                    States = {
                      GenerateSoilTemperatureAccessibleContent = {
                        Type     = "Task"
                        Resource = var.management_generate_accessible_contents_lambda_arn
                        Next     = "AccessibilityChoice"
                      }
                      AccessibilityChoice = {
                        Type = "Choice"
                        Choices = [
                          {
                            Variable = "$.type"
                            StringEquals = "text_to_speech"
                            Next = "TextToSpeech"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "image_recognition"
                            Next = "ImageRecognition"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "video_caption"
                            Next = "VideoCaption"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "text_simplification"
                            Next = "TextSimplification"
                          }
                        ]
                        Default = "AccessibilityEnd"
                      },
                      TextToSpeech = {
                        Type     = "Task"
                        Resource = var.accessible_text_to_speech_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      ImageRecognition = {
                        Type     = "Task"
                        Resource = var.accessible_image_recognition_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      VideoCaption = {
                        Type     = "Task"
                        Resource = var.accessible_video_caption_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      TextSimplification = {
                        Type     = "Task"
                        Resource = var.accessible_text_simplification_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      AccessibilityEnd = {
                        Type = "Pass"
                        End  = true
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
                  {
                    StartAt = "GenerateAirMoistureAccessibleContent"
                    States = {
                      GenerateAirMoistureAccessibleContent = {
                        Type     = "Task"
                        Resource = var.management_generate_accessible_contents_lambda_arn
                        Next     = "AccessibilityChoice"
                      }
                      AccessibilityChoice = {
                        Type = "Choice"
                        Choices = [
                          {
                            Variable = "$.type"
                            StringEquals = "text_to_speech"
                            Next = "TextToSpeech"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "image_recognition"
                            Next = "ImageRecognition"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "video_caption"
                            Next = "VideoCaption"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "text_simplification"
                            Next = "TextSimplification"
                          }
                        ]
                        Default = "AccessibilityEnd"
                      },
                      TextToSpeech = {
                        Type     = "Task"
                        Resource = var.accessible_text_to_speech_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      ImageRecognition = {
                        Type     = "Task"
                        Resource = var.accessible_image_recognition_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      VideoCaption = {
                        Type     = "Task"
                        Resource = var.accessible_video_caption_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      TextSimplification = {
                        Type     = "Task"
                        Resource = var.accessible_text_simplification_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      AccessibilityEnd = {
                        Type = "Pass"
                        End  = true
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
                  {
                    StartAt = "GenerateAirTemperatureAccessibleContent"
                    States = {
                      GenerateAirTemperatureAccessibleContent = {
                        Type     = "Task"
                        Resource = var.management_generate_accessible_contents_lambda_arn
                        Next     = "AccessibilityChoice"
                      }
                      AccessibilityChoice = {
                        Type = "Choice"
                        Choices = [
                          {
                            Variable = "$.type"
                            StringEquals = "text_to_speech"
                            Next = "TextToSpeech"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "image_recognition"
                            Next = "ImageRecognition"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "video_caption"
                            Next = "VideoCaption"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "text_simplification"
                            Next = "TextSimplification"
                          }
                        ]
                        Default = "AccessibilityEnd"
                      },
                      TextToSpeech = {
                        Type     = "Task"
                        Resource = var.accessible_text_to_speech_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      ImageRecognition = {
                        Type     = "Task"
                        Resource = var.accessible_image_recognition_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      VideoCaption = {
                        Type     = "Task"
                        Resource = var.accessible_video_caption_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      TextSimplification = {
                        Type     = "Task"
                        Resource = var.accessible_text_simplification_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      AccessibilityEnd = {
                        Type = "Pass"
                        End  = true
                      }
                    }
                  }
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
                  {
                    StartAt = "GenerateBrightnessAccessibleContent"
                    States = {
                      GenerateBrightnessAccessibleContent = {
                        Type     = "Task"
                        Resource = var.management_generate_accessible_contents_lambda_arn
                        Next     = "AccessibilityChoice"
                      }
                      AccessibilityChoice = {
                        Type = "Choice"
                        Choices = [
                          {
                            Variable = "$.type"
                            StringEquals = "text_to_speech"
                            Next = "TextToSpeech"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "image_recognition"
                            Next = "ImageRecognition"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "video_caption"
                            Next = "VideoCaption"
                          },
                          {
                            Variable = "$.type"
                            StringEquals = "text_simplification"
                            Next = "TextSimplification"
                          }
                        ]
                        Default = "AccessibilityEnd"
                      },
                      TextToSpeech = {
                        Type     = "Task"
                        Resource = var.accessible_text_to_speech_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      ImageRecognition = {
                        Type     = "Task"
                        Resource = var.accessible_image_recognition_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      VideoCaption = {
                        Type     = "Task"
                        Resource = var.accessible_video_caption_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      TextSimplification = {
                        Type     = "Task"
                        Resource = var.accessible_text_simplification_lambda_arn
                        Next     = "AccessibilityEnd"
                      },
                      AccessibilityEnd = {
                        Type = "Pass"
                        End  = true
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
                Resource = var.tasks_management_lambda_arn
                End      = true
              }
            }
          }
        ]
        Next = "MergeBranchResults"
      },
      MergeBranchResults = {
        Type     = "Task"
        Resource = var.tasks_results_merge_lambda_arn
        Next     = "HandleAgrixInteractions"
      },
      HandleAgrixInteractions = {
        Type = "Task",
        Resource = var.agrix_interaction_handler_feature_lambda_arn
        Next = "ProcessAgrixFulfillments"
      },
      ProcessAgrixFulfillments = {
        Type = "Task",
        Resource = var.agrix_interaction_handler_feature_lambda_arn,
        Parameters = {
          "input.$": "$",
          "handlers": {
            "advanced_sensor_handler": {
              "fulfillment": var.advanced_sensor_handler_feature_fulfillment_lambda_arn,
              "main": var.advanced_sensor_handler_feature_lambda_arn
            },
            "ar_processor_handler": {
              "fulfillment": var.ar_processor_handler_feature_fulfillment_lambda_arn,
              "main": var.ar_processor_handler_feature_lambda_arn
            },
            "compliance_assistance_handler": {
              "fulfillment": var.compliance_assistance_handler_feature_fulfillment_lambda_arn,
              "main": var.compliance_assistance_handler_feature_lambda_arn
            },
            "crop_planning_handler": {
              "fulfillment": var.crop_planning_handler_feature_fulfillment_lambda_arn,
              "main": var.crop_planning_handler_feature_lambda_arn
            },
            "dynamic_personlization_handler": {
              "fulfillment": var.dynamic_personlization_handler_feature_fulfillment_lambda_arn,
              "main": var.dynamic_personlization_handler_feature_lambda_arn
            },
            "image_diagnosis_handler": {
              "fulfillment": var.image_diagnosis_handler_feature_fulfillment_lambda_arn,
              "main": var.image_diagnosis_handler_feature_lambda_arn
            },
            "knowledge_sharing_handler": {
              "fulfillment": var.knowledge_sharing_handler_feature_fulfillment_lambda_arn,
              "main": var.knowledge_sharing_handler_feature_lambda_arn
            },
            "learning_module_handler": {
              "fulfillment": var.learning_module_handler_feature_fulfillment_lambda_arn,
              "main": var.learning_module_handler_feature_lambda_arn
            },
            "marketing_assistant_handler": {
              "fulfillment": var.marketing_assistant_handler_feature_fulfillment_lambda_arn,
              "main": var.marketing_assistant_handler_feature_lambda_arn
            },
            "marketplace_handler": {
              "fulfillment": var.marketplace_handler_feature_fulfillment_lambda_arn,
              "main": var.marketplace_handler_feature_lambda_arn
            },
            "predictive_analysis_handler": {
              "fulfillment": var.predictive_analysis_handler_feature_fulfillment_lambda_arn,
              "main": var.predictive_analysis_handler_feature_lambda_arn
            },
            "report_generator_handler": {
              "fulfillment": var.report_generator_handler_feature_fulfillment_lambda_arn,
              "main": var.report_generator_handler_feature_lambda_arn
            },
            "scenario_simulator_handler": {
              "fulfillment": var.scenario_simulator_handler_feature_fulfillment_lambda_arn,
              "main": var.scenario_simulator_handler_feature_lambda_arn
            },
            "sustainability_assistant_handler": {
              "fulfillment": var.sustainability_assistant_handler_feature_fulfillment_lambda_arn,
              "main": var.sustainability_assistant_handler_feature_lambda_arn
            },
            "voice_assistant_handler": {
              "fulfillment": var.voice_assistant_handler_feature_fulfillment_lambda_arn,
              "main": var.voice_assistant_handler_feature_lambda_arn
            }
          }
        },
        End = true
      }
    }
  })
}