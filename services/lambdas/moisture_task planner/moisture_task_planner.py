import json
import boto3
from datetime import datetime, timedelta
import base64
import uuid
import os

# Inicialização dos clientes AWS
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
lambda_client = boto3.client('lambda')
kinesis_video = boto3.client('kinesisvideo')

# Obter o nome do Kinesis Video Stream da variável de ambiente
KINESIS_VIDEO_STREAM_NAME = os.environ['KINESIS_VIDEO_STREAM_NAME']

# Nome do bucket S3 para armazenar mídias
S3_BUCKET_NAME = "task-planner-media-bucket"

def lambda_handler(event, context):
    # Verifica se o evento é do DynamoDB Stream da tabela AverageMoisture
    if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:dynamodb':
        return process_average_moisture_event(event)
    
    # Se não for um evento do DynamoDB Stream, processa como uma requisição HTTP
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
    elif http_method == 'POST':
        if path == '/generate-task-plan':
            return generate_new_task_plan()

    # Retorna 404 se nenhuma rota corresponder
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found'})
    }

def process_average_moisture_event(event):
    for record in event['Records']:
        if record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY':
            new_image = record['dynamodb']['NewImage']
            
            if 'averageMoisture' in new_image and 'timestamp' in new_image:
                new_average_moisture = float(new_image['averageMoisture']['N'])
                timestamp = new_image['timestamp']['S']
                
                # Aqui você pode adicionar lógica adicional se necessário
                # Por exemplo, verificar se a mudança é significativa o suficiente para gerar um novo plano
                
                # Gerar novo plano de tarefas
                return generate_new_task_plan()

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído sem necessidade de gerar novo plano')
    }

def get_latest_task_plan():
    # Busca o plano de tarefas mais recente do DynamoDB
    response = dynamodb.query(
        TableName='TaskPlans',
        Limit=1,
        ScanIndexForward=False,
        KeyConditionExpression='#pk = :pk',
        ExpressionAttributeNames={'#pk': 'PK'},
        ExpressionAttributeValues={':pk': {'S': 'TASK_PLAN'}}
    )
    if 'Items' in response and response['Items']:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'][0])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No task plan found'})
        }

def get_images():
    # Busca as URLs das imagens mais recentes do S3
    response = s3.list_objects_v2(Bucket='your-image-bucket', Prefix='task-plan-images/', MaxKeys=10)
    image_urls = [f"https://your-image-bucket.s3.amazonaws.com/{obj['Key']}" for obj in response.get('Contents', [])]
    return {
        'statusCode': 200,
        'body': json.dumps(image_urls)
    }

def get_videos():
    # Busca as URLs dos vídeos mais recentes do S3
    response = s3.list_objects_v2(Bucket='your-video-bucket', Prefix='task-plan-videos/', MaxKeys=10)
    video_urls = [f"https://your-video-bucket.s3.amazonaws.com/{obj['Key']}" for obj in response.get('Contents', [])]
    return {
        'statusCode': 200,
        'body': json.dumps(video_urls)
    }

def generate_new_task_plan():
    # Obtém os dados mais recentes de umidade média e recomendações
    moisture_data, recommendations = get_latest_data()
    
    # Gera um novo plano de tarefas usando IA
    task_plan = generate_task_plan_with_ai(moisture_data, recommendations)
    
    # Gera novas mídias (imagens e vídeos) para o plano de tarefas
    media_urls = generate_media(task_plan)
    
    # Armazena o novo plano de tarefas e as URLs das mídias no DynamoDB
    store_task_plan(task_plan, media_urls)

    # Retorna o novo plano de tarefas e as URLs das mídias
    return {
        'statusCode': 200,
        'body': json.dumps({
            'taskPlan': task_plan,
            'mediaUrls': media_urls
        })
    }

def generate_task_plan_with_ai(moisture_data, recommendations):
    # Prepara o prompt para a IA com base nos dados de umidade média e recomendações
    prompt = f"""
    Com base nos seguintes dados de umidade média do solo e recomendações:
    Umidade Média: {moisture_data['averageMoisture']}
    Timestamp: {moisture_data['timestamp']}
    Recomendações:
    {json.dumps(recommendations, indent=2)}

    Gere um plano detalhado de tarefas para as próximas 4 semanas, incluindo:
    1. Datas e horários recomendados para colheita
    2. Datas e horários recomendados para plantio
    3. Atividades de manutenção necessárias
    4. Recomendações de irrigação

    Forneça um plano estruturado com datas específicas e descrições das tarefas.
    """

    # Chama o modelo de IA (neste caso, usando o Bedrock da AWS)
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

    # Processa a resposta da IA
    bedrock_response = json.loads(response['body'].read())
    return bedrock_response['completions'][0]['data']['text']

def get_latest_data():
    # Busca o dado mais recente da tabela AverageMoisture
    moisture_response = dynamodb.query(
        TableName='AverageMoisture',
        Limit=1,
        ScanIndexForward=False,
        KeyConditionExpression='#pk = :pk',
        ExpressionAttributeNames={'#pk': 'PK'},
        ExpressionAttributeValues={':pk': {'S': 'MOISTURE'}}
    )
    moisture_data = moisture_response['Items'][0] if moisture_response['Items'] else None

    # Busca as recomendações mais recentes
    recommendations = {}
    if moisture_data:
        state = moisture_data.get('state', {}).get('S', 'default')
        recommendations_response = dynamodb.query(
            TableName='RecommendationsByTopic',
            KeyConditionExpression='state = :state',
            ExpressionAttributeValues={':state': {'S': state}},
            ScanIndexForward=False,
            Limit=10  # Obtém as 10 recomendações mais recentes
        )
        for item in recommendations_response.get('Items', []):
            recommendations[item['topic']['S']] = item['recommendation']['S']

    return moisture_data, recommendations

def generate_media(task_plan):
    images = []
    videos = []

    # Gerar imagens para cada tarefa no plano
    tasks = parse_task_plan(task_plan)
    for task in tasks:
        image_prompt = f"Agricultural scene showing {task['description']}"
        image_url = generate_and_upload_image(image_prompt)
        images.append(image_url)

        # Gerar um vídeo simples a partir da imagem
        video_url = generate_and_upload_video(image_url, task['description'])
        videos.append(video_url)

    return {
        'images': images,
        'videos': videos
    }

def parse_task_plan(task_plan):
    # Esta função deve analisar o texto do plano de tarefas e extrair as tarefas individuais
    # Por simplicidade, vamos assumir que cada linha é uma tarefa separada
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
    # Obter o endpoint para o Kinesis Video Stream
    endpoint = kinesis_video.get_data_endpoint(
        APIName='PUT_MEDIA',
        StreamName=KINESIS_VIDEO_STREAM_NAME
    )['DataEndpoint']
    
    # Criar um cliente Kinesis Video usando o endpoint
    kvs = boto3.client('kinesis-video-media', endpoint_url=endpoint)
    
    # Baixar a imagem do S3
    image_key = image_url.split('/')[-1]
    s3.download_file(S3_BUCKET_NAME, image_key, '/tmp/image.png')
    
    # Simular a criação de um vídeo (na prática, você usaria uma biblioteca como OpenCV ou MoviePy)
    with open('/tmp/image.png', 'rb') as image_file:
        image_data = image_file.read()
    
    # Simular um vídeo repetindo a imagem por alguns segundos
    video_data = image_data * 30  # Repete a imagem 30 vezes para simular um vídeo de alguns segundos
    
    # Upload do "vídeo" para o Kinesis Video Stream
    kvs.put_media(
        StreamName=KINESIS_VIDEO_STREAM_NAME,
        Data=video_data,
        ContentType='video/h264'
    )
    
    # Na prática, você processaria o vídeo com Rekognition aqui
    # Por simplicidade, vamos apenas salvar o "vídeo" no S3
    video_key = f"generated_video_{uuid.uuid4()}.mp4"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=video_key,
        Body=video_data,
        ContentType='video/mp4'
    )
    
    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{video_key}"

def store_task_plan(task_plan, media_urls):
    # Armazena o plano de tarefas e as URLs das mídias no DynamoDB
    timestamp = datetime.utcnow().isoformat()
    dynamodb.put_item(
        TableName='TaskPlans',
        Item={
            'timestamp': {'S': timestamp},
            'taskPlan': {'S': task_plan},
            'mediaUrls': {'M': {
                'images': {'L': [{'S': url} for url in media_urls['images']]},
                'videos': {'L': [{'S': url} for url in media_urls['videos']]}
            }}
        }
    )
    
    # Atualiza o item 'latest' para facilitar a recuperação do plano mais recente
    dynamodb.put_item(
        TableName='TaskPlans',
        Item={
            'timestamp': {'S': 'latest'},
            'taskPlan': {'S': task_plan},
            'mediaUrls': {'M': {
                'images': {'L': [{'S': url} for url in media_urls['images']]},
                'videos': {'L': [{'S': url} for url in media_urls['videos']]}
            }}
        }
    )