import json
import boto3
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from botocore.exceptions import ClientError
import base64
import uuid
import os

# Inicialização dos clientes AWS
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
kinesis_video = boto3.client('kinesisvideo')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

# Obter o nome do Kinesis Video Stream da variável de ambiente
KINESIS_VIDEO_STREAM_NAME = 'task_planner_video_stream'

# Nome do bucket S3 para armazenar mídias
S3_BUCKET_NAME = "task-planner-media-bucket"

# Constantes para o planejamento de tarefas
MOISTURE_THRESHOLD = 5.0  # Diferença de umidade que aciona um novo plano
TIME_THRESHOLD = timedelta(hours=6)  # Tempo mínimo entre novos planos

# Data atual
current_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

# Tabelas do DynamoDB
task_plan_table = dynamodb.Table('TaskPlans')
moisture_history_table = dynamodb.Table('MoistureHistory')

# Nome da coisa IoT
IOT_THING_NAME = os.environ.get('IOT_THING_NAME', 'moisture_sensor')

def lambda_handler(event, context):
    if 'moisture' in event and 'status' in event:
        return process_iot_event(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid event format'})
        }

def process_iot_event(event):
    moisture = event['moisture']
    status = event['status']
    timestamp = datetime.now(timezone.utc).isoformat()

    # Armazena os dados do IoT no DynamoDB
    moisture_history_table.put_item(Item={
        'timestamp': timestamp,
        'moisture': str(moisture),
        'date': timestamp.split('T')[0],
        'status': status
    })

    # Verifica se deve gerar um novo plano de tarefas
    if should_generate_new_plan(moisture, timestamp):
        new_plan = generate_new_task_plan()
        store_task_plan(new_plan, timestamp, moisture)
        return {
            'statusCode': 200,
            'body': json.dumps('Novo plano de tarefas gerado e armazenado')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Dados do IoT processados com sucesso')
    }

def should_generate_new_plan(new_moisture, timestamp):
    last_plan = get_last_task_plan()
    
    if not last_plan:
        return True
    
    last_plan_timestamp = datetime.fromisoformat(last_plan['CreatedAt'])
    current_timestamp = datetime.fromisoformat(timestamp)
    
    if current_timestamp - last_plan_timestamp < TIME_THRESHOLD:
        return False
    
    last_moisture = float(last_plan['AverageMoisture'])
    if abs(new_moisture - last_moisture) >= MOISTURE_THRESHOLD:
        return True
    
    return False

def get_last_task_plan():
    response = task_plan_table.query(
        IndexName='TaskPlanIndex',
        KeyConditionExpression='TaskPlan = :tp',
        ExpressionAttributeValues={':tp': 'latest'},
        ScanIndexForward=False,
        Limit=1
    )
    items = response.get('Items', [])
    return items[0] if items else None

def parse_task_plan(task_plan_text):
    tasks = []
    current_date = None
    for line in task_plan_text.split('\n'):
        line = line.strip()
        if line:
            if ':' in line:
                # This line likely contains a date
                current_date = line.split(':')[0].strip()
            else:
                # This line contains a task
                tasks.append({
                    'date': current_date,
                    'task': line
                })
    return tasks

def generate_new_task_plan():
    moisture_data, recommendations = get_latest_data()
    task_plan = generate_task_plan_with_ai(moisture_data, recommendations)
    media_urls = generate_media(task_plan)
    return {
        'taskPlan': task_plan,
        'mediaUrls': media_urls
    }

def generate_task_plan_with_ai(moisture_data, recommendations):
    realtime_moisture = get_realtime_moisture()
    realtime_moisture_data = json.loads(realtime_moisture['body'])

    prompt = f"""
    Com base nos seguintes dados de umidade do solo e recomendações:
    Umidade Atual: {moisture_data['moisture']}
    Umidade em Tempo Real: {realtime_moisture_data['moisture']}
    Timestamp: {realtime_moisture_data['timestamp']}
    Recomendações:
    {json.dumps(recommendations, indent=2)}

    Gere um plano detalhado de tarefas para as próximas 4 semanas, incluindo:
    1. Datas e horários recomendados para colheita
    2. Datas e horários recomendados para plantio
    3. Atividades de manutenção necessárias
    4. Recomendações de irrigação

    Forneça um plano estruturado com datas específicas e descrições das tarefas.
    Leve em consideração a diferença entre a umidade atual e a umidade em tempo real ao fazer as recomendações.
    """

    response = bedrock.invoke_model(
        modelId='ai21.j2-mid-v1',
        body=json.dumps({
            "prompt": prompt,
            "maxTokens": 1000,
            "temperature": 0.7,
            "topP": 1,
            "stopSequences": [],
            "countPenalty": {"scale": 0},
            "presencePenalty": {"scale": 0},
            "frequencyPenalty": {"scale": 0}
        })
    )

    bedrock_response = json.loads(response['body'].read())
    task_plan_text = bedrock_response['completions'][0]['data']['text']
    
    # Parse the task plan into an array of tasks
    tasks = parse_task_plan(task_plan_text)
    
    return tasks

def get_latest_data():
    moisture_response = moisture_history_table.query(
        KeyConditionExpression='timestamp <= :now',
        ExpressionAttributeValues={':now': datetime.now(timezone.utc).isoformat()},
        ScanIndexForward=False,
        Limit=1
    )
    moisture_data = moisture_response['Items'][0] if moisture_response['Items'] else None

    recommendations = {}
    if moisture_data:
        state = moisture_data.get('status', 'default')
        recommendations_response = dynamodb.Table('RecommendationsByTopic').query(
            KeyConditionExpression='state = :state',
            ExpressionAttributeValues={':state': state},
            ScanIndexForward=False,
            Limit=10
        )
        for item in recommendations_response.get('Items', []):
            recommendations[item['topic']] = item['recommendation']

    return moisture_data, recommendations

def generate_media(task_plan):
    images = []
    videos = []

    for task in task_plan:
        image_prompt = f"Agricultural scene showing {task['task']}"
        image_url = generate_and_upload_image(image_prompt)
        images.append(image_url)

        video_url = generate_and_upload_video(image_url, task['task'])
        videos.append(video_url)

    return {
        'images': images,
        'videos': videos
    }

def parse_task_plan(task_plan):
    tasks = []
    for line in task_plan.split('\n'):
        if line.strip():
            tasks.append({'description': line.strip()})
    return tasks

def generate_and_upload_image(prompt):
    response = bedrock.invoke_model(
        modelId='stability.stable-diffusion-xl',
        body=json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 10,
            "steps": 50,
            "width": 512,
            "height": 512
        })
    )

    response_body = json.loads(response['body'].read())
    image_data = base64.b64decode(response_body['artifacts'][0]['base64'])
    
    file_name = f"generated_image_{uuid.uuid4()}.png"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=image_data,
        ContentType='image/png'
    )

    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

def generate_and_upload_video(image_url, description):
    endpoint = kinesis_video.get_data_endpoint(
        APIName='PUT_MEDIA',
        StreamName=KINESIS_VIDEO_STREAM_NAME
    )['DataEndpoint']
    
    kvs = boto3.client('kinesis-video-media', endpoint_url=endpoint)
    
    image_key = image_url.split('/')[-1]
    s3.download_file(S3_BUCKET_NAME, image_key, '/tmp/image.png')
    
    with open('/tmp/image.png', 'rb') as image_file:
        image_data = image_file.read()
    
    video_data = image_data * 30
    
    kvs.put_media(
        StreamName=KINESIS_VIDEO_STREAM_NAME,
        Data=video_data,
        ContentType='video/h264'
    )
    
    video_key = f"generated_video_{uuid.uuid4()}.mp4"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=video_key,
        Body=video_data,
        ContentType='video/mp4'
    )
    
    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{video_key}"

def store_task_plan(task_plan, timestamp, average_moisture):
    plan_id = str(uuid.uuid4())
    storage_date = datetime.now(timezone.utc).date().isoformat()
    
    task_plan_array = []
    for task in task_plan['taskPlan']:
        task_plan_array.append({
            'date': task['date'],
            'task': task['task'],
            'storedAt': storage_date
        })
    
    item = {
        'PlanId': plan_id,
        'CreatedAt': timestamp,
        'TaskPlan': json.dumps(task_plan_array),  # Convertendo para JSON string
        'MediaUrls': json.dumps(task_plan['mediaUrls']),  # Convertendo para JSON string
        'AverageMoisture': Decimal(str(average_moisture)),
        'UserId': 'default_user'
    }
    
    task_plan_table.put_item(Item=item)
    
    latest_item = item.copy()
    latest_item['TaskPlan'] = 'latest'
    task_plan_table.put_item(Item=latest_item)
    
    moisture_history_table.put_item(Item={
        'timestamp': timestamp,
        'averageMoisture': Decimal(str(average_moisture)),
        'planGenerated': 'Yes'
    })

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
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to retrieve real-time data',
                'details': str(e)
            })
        }