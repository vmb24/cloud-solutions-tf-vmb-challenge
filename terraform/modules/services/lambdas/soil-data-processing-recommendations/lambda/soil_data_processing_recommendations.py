import json
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from decimal import Decimal

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

IOT_THING_NAME = 'moisture_sensor'
DYNAMODB_TABLE_NAME = 'AgriculturalRecommendations'
MOISTURE_DATA_TABLE_NAME = 'MoistureAverages'

TOPICS = [
    "Necessidade de Irrigação",
    "Índice de Estresse Hídrico",
    "Prevenção de Doenças",
    "Eficiência no Uso da Água",
    "Análise de Retenção de Água do Solo",
    "Previsão de Colheita",
    "Planejamento de Plantio",
    "Avaliação do Impacto das Chuvas",
    "Modelagem de Crescimento das Plantas",
    "Detecção de Zonas de Solo Deficiente"
]

def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, indent=2))

    if 'httpMethod' in event and 'path' in event:
        return handle_api_gateway_event(event)
    elif 'moisture' in event:
        return process_moisture_data(event)
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Requisição inválida'})
    }

def handle_api_gateway_event(event):
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'GET':
        if path == '/moisture':
            return get_latest_moisture()
        elif path == '/moisture/history':
            return get_moisture_history()
        elif path == '/recommendations':
            return get_all_recommendations()
        elif path.startswith('/recommendation/'):
            topic = path.split('/')[-1]
            return get_latest_recommendation(topic)

    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Requisição inválida'})
    }

def get_latest_moisture():
    try:
        print(f"Tentando obter shadow para o dispositivo: {IOT_THING_NAME}")
        response = iot_client.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode())
        print(f"Payload do shadow recebido: {payload}")
        state = payload['state']['reported']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'moisture': state['moisture'],
                'status': state['status'],
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        print(f"Erro ao obter shadow do dispositivo: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao chamar a operação GetThingShadow: {str(e)}"})
        }

def process_moisture_data(event):
    try:
        moisture = event['moisture']
        status = event['status']
        timestamp = datetime.now().isoformat()

        store_average_moisture(moisture, status, timestamp)

        generate_all_recommendations(moisture, status)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Dados de umidade processados e recomendações geradas'})
        }
    except Exception as e:
        print(f"Erro ao processar dados de umidade: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Falha ao processar dados de umidade: {str(e)}"})
        }

def store_average_moisture(moisture, status, timestamp):
    table = dynamodb.Table(MOISTURE_DATA_TABLE_NAME)
    table.put_item(
        Item={
            'date': timestamp.split('T')[0],
            'timestamp': timestamp,
            'thing_name': IOT_THING_NAME,
            'moisture': Decimal(str(moisture)),  # Convertendo para Decimal
            'status': status
        }
    )

def get_moisture_history(days=30):
    table = dynamodb.Table(MOISTURE_DATA_TABLE_NAME)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    response = table.query(
        KeyConditionExpression=Key('date').between(start_date.isoformat(), end_date.isoformat())
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def generate_all_recommendations(moisture, status):
    results = {}
    for topic in TOPICS:
        result = generate_recommendation_for_topic(topic, moisture, status)
        results[topic] = json.loads(result['body'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

def generate_recommendation_for_topic(topic, moisture, status):
    print(f"Gerando recomendação para o tópico: {topic}")
    if topic not in TOPICS:
        print(f"Tópico inválido: {topic}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Tópico inválido'})
        }

    prompt = f"""
    Human: Você é um especialista em agricultura. Forneça uma recomendação detalhada para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Umidade atual do solo: {moisture}%
    - Status atual: {status}

    Forneça uma recomendação prática e acionável para o seguinte tópico:
    {topic}

    A recomendação deve ser específica, detalhada e diretamente relacionada ao nível de umidade atual. Responda em português.

    Assistant: Baseado nos dados fornecidos, aqui está minha recomendação para {topic}:

    Human: Obrigado. Por favor, forneça apenas a recomendação, sem incluir nenhum texto introdutório ou conclusivo.

    Assistant:"""

    print(f"Enviando requisição para o Bedrock com o prompt: {prompt}")
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 300,
                "temperature": 0.5,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"]
            })
        )
        print(f"Resposta do Bedrock: {response}")
    except Exception as e:
        print(f"Erro ao chamar o Bedrock: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao gerar recomendação: {str(e)}'})
        }

    recommendation = json.loads(response['body'].read())['completion'].strip()
    print(f"Recomendação gerada: {recommendation}")

    timestamp = datetime.now().isoformat()

    try:
        store_recommendation(topic, recommendation, moisture, status, timestamp)
        print("Recomendação armazenada com sucesso")
    except Exception as e:
        print(f"Erro ao armazenar recomendação: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao armazenar recomendação: {str(e)}'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'topic': topic,
            'recommendation': recommendation,
            'moisture': moisture,
            'status': status,
            'timestamp': timestamp
        })
    }

def store_recommendation(topic, recommendation, moisture, status, timestamp):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={
            'topic': topic,
            'timestamp': timestamp,
            'recommendation': recommendation,
            'moisture': Decimal(str(moisture)),  # Convertendo para Decimal
            'status': status
        }
    )

def get_all_recommendations():
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def get_latest_recommendation(topic):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('topic').eq(topic),
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
            'body': json.dumps({'error': 'Recomendação não encontrada'})
        }