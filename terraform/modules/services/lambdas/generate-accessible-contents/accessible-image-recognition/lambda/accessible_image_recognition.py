import boto3
import json

def lambda_handler(event, context):
    rekognition_client = boto3.client('rekognition')
    
    bucket = event['bucket']
    image_key = event['image_key']
    
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image_key
            }
        },
        MaxLabels=10
    )
    
    labels = [label['Name'] for label in response['Labels']]
    description = "A imagem contém: " + ", ".join(labels)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'description': description})
    }