import json
import boto3
from datetime import datetime, timezone
import os

# Inicialização dos clientes AWS
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

# Nome do bucket S3 para armazenar mídias
S3_BUCKET_NAME = "task-planner-media-bucket"

# Tabelas do DynamoDB
task_plan_table = dynamodb.Table('TaskPlans')
moisture_history_table = dynamodb.Table('MoistureHistory')

# Nome da coisa IoT
IOT_THING_NAME = os.environ.get('IOT_THING_NAME', 'moisture_sensor')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']

    # Roteamento das requisições baseado no método HTTP e caminho
    if http_method == 'GET':
        if path == '/task-plan':
            return get_latest_task_plan()
        elif path == '/images':
            return get_images()
        elif path == '/videos':
            return get_videos()
        elif path == '/realtime-moisture':
            return get_realtime_moisture()
    elif http_method == 'POST':
        if path == '/generate-task-plan':
            return generate_new_task_plan()

    # Retorna 404 se nenhuma rota corresponder
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found'})
    }

def get_latest_task_plan():
    response = task_plan_table.query(
        IndexName='TaskPlanIndex',
        KeyConditionExpression='TaskPlan = :tp',
        ExpressionAttributeValues={':tp': 'latest'},
        ScanIndexForward=False,
        Limit=1
    )
    items = response.get('Items', [])
    if items:
        return {
            'statusCode': 200,
            'body': json.dumps(items[0])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No task plan found'})
        }

def get_images():
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='task-plan-images/', MaxKeys=10)
    image_urls = [f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{obj['Key']}" for obj in response.get('Contents', [])]
    return {
        'statusCode': 200,
        'body': json.dumps(image_urls)
    }

def get_videos():
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='task-plan-videos/', MaxKeys=10)
    video_urls = [f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{obj['Key']}" for obj in response.get('Contents', [])]
    return {
        'statusCode': 200,
        'body': json.dumps(video_urls)
    }

def get_realtime_moisture():
    try:
        response = iot_client.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode('utf-8'))
        current_moisture = payload['state']['reported']['moisture']
        current_status = payload['state']['reported']['status']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'moisture': current_moisture,
                'status': current_status
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to retrieve real-time data',
                'details': str(e)
            })
        }

def generate_new_task_plan():
    # Esta função agora invocará a outra função Lambda
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='moisture_task_planner',
        InvocationType='RequestResponse',
        Payload=json.dumps({})
    )
    
    result = json.loads(response['Payload'].read())
    
    if result.get('statusCode') == 200:
        return {
            'statusCode': 200,
            'body': result['body']
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to generate new task plan'})
        }