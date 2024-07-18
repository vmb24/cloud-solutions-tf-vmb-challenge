import json
import boto3
from handlers.image_analysis_handler import ImageAnalysisHandler

def lambda_handler(event, context):
    handler = ImageAnalysisHandler()
    return handler.handle(event, context)
