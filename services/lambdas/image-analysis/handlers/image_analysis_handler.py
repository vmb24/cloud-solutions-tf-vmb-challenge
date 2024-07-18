import boto3
import json

class ImageAnalysisHandler:
    def __init__(self):
        self.rekognition_client = boto3.client('rekognition')
        self.s3_client = boto3.client('s3')

    def handle(self, event, context):
        try:
            bucket = event['Records'][0]['s3']['bucket']['name']
            key = event['Records'][0]['s3']['object']['key']
            response = self.rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                MaxLabels=10,
                MinConfidence=75
            )
            labels = response['Labels']
            return {
                'statusCode': 200,
                'body': json.dumps(labels)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
