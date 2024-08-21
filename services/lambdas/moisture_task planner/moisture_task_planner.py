import json
import boto3
from datetime import datetime, timedelta
import base64
import uuid

# Inicialização dos clientes AWS
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
lambda_client = boto3.client('lambda')

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
    
    bucket_name = 'your-s3-bucket-name'
    file_name = f"generated_image_{uuid.uuid4()}.png"
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=image_data,
        ContentType='image/png'
    )

    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"

def generate_and_upload_video(image_url, description):
    # Usar Rekognition para criar um vídeo simples a partir da imagem
    response = rekognition.start_segment_detection(
        Video={'S3Object': {'Bucket': 'your-s3-bucket-name', 'Name': image_url.split('/')[-1]}},
        SegmentTypes=['TECHNICAL_CUE'],
        Filters={'TechnicalCueFilter': {'MinSegmentConfidence': 80}}
    )

    job_id = response['JobId']

    # Esperar até que o trabalho seja concluído
    while True:
        response = rekognition.get_segment_detection(JobId=job_id)
        status = response['JobStatus']
        if status in ['SUCCEEDED', 'FAILED']:
            break

    if status == 'SUCCEEDED':
        # Salvar o vídeo no S3
        bucket_name = 'your-s3-bucket-name'
        video_name = f"generated_video_{uuid.uuid4()}.mp4"
        s3.put_object(
            Bucket=bucket_name,
            Key=video_name,
            Body=response['VideoMetadata']['Codec'],
            ContentType='video/mp4'
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{video_name}"
    else:
        return None

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