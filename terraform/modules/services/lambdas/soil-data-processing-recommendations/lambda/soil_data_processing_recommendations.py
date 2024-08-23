import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

IOT_THING_NAME = 'moisture_sensor'
DYNAMODB_TABLE_NAME = 'AgriculturalRecommendations'

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
    print("Received event:", json.dumps(event, indent=2))

    if 'httpMethod' in event and 'path' in event:
        return handle_api_gateway_event(event)
    
    return generate_all_recommendations()

def handle_api_gateway_event(event):
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'GET':
        if path == '/moisture':
            return get_latest_moisture()
        elif path == '/recommendations':
            return get_all_recommendations()
        elif path.startswith('/recommendation/'):
            topic = path.split('/')[-1]
            return get_latest_recommendation(topic)
    elif http_method == 'POST':
        if path == '/generate-recommendation':
            body = json.loads(event.get('body', '{}'))
            topic = body.get('topic')
            return generate_recommendation_for_topic(topic)
        elif path == '/generate-all-recommendations':
            return generate_all_recommendations()

    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid request'})
    }

def get_latest_moisture():
    """
    Obtém o dado de umidade mais recente do IoT Core.
    """
    try:
        print(f"Attempting to get shadow for thing: {IOT_THING_NAME}")
        response = iot_client.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode())
        print(f"Received shadow payload: {payload}")
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
        print(f"Error getting thing shadow: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"An error occurred when calling the GetThingShadow operation: {str(e)}"})
        }

def generate_recommendation_for_topic(topic):
    print(f"Generating recommendation for topic: {topic}")
    if topic not in TOPICS:
        print(f"Invalid topic: {topic}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid topic'})
        }

    moisture_data = get_latest_moisture()
    print(f"Moisture data: {moisture_data}")
    if moisture_data['statusCode'] != 200:
        print(f"Failed to get moisture data: {moisture_data}")
        return moisture_data

    moisture_info = json.loads(moisture_data['body'])
    current_moisture = moisture_info['moisture']
    current_status = moisture_info['status']
    timestamp = moisture_info['timestamp']

    prompt = f"""
    Você é um especialista em agricultura. Forneça uma recomendação detalhada para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Umidade atual do solo: {current_moisture}%
    - Status atual: {current_status}

    Forneça uma recomendação prática e acionável para o seguinte tópico:
    {topic}

    A recomendação deve ser específica, detalhada e diretamente relacionada ao nível de umidade atual.
    """

    print(f"Sending request to Bedrock with prompt: {prompt}")
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "top_p": 0.9,
            })
        )
        print(f"Bedrock response: {response}")
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to generate recommendation: {str(e)}'})
        }

    recommendation = json.loads(response['body'].read())['completion'].strip()
    print(f"Generated recommendation: {recommendation}")

    try:
        store_recommendation(topic, recommendation, current_moisture, current_status, timestamp)
        print("Recommendation stored successfully")
    except Exception as e:
        print(f"Error storing recommendation: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to store recommendation: {str(e)}'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'topic': topic,
            'recommendation': recommendation,
            'moisture': current_moisture,
            'status': current_status,
            'timestamp': timestamp
        })
    }


def store_recommendation(topic, recommendation, moisture, status, timestamp):
    """
    Armazena a recomendação gerada na tabela AgriculturalRecommendations.
    """
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={
            'timestamp': timestamp,
            'thing_name': IOT_THING_NAME,
            'topic': topic,
            'recommendation': recommendation,
            'moisture': moisture,
            'status': status
        }
    )

def get_latest_recommendation(topic):
    """
    Retorna a recomendação mais recente para um tópico específico.
    """
    if topic not in TOPICS:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid topic'})
        }

    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.query(
        IndexName='TopicIndex',
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
            'body': json.dumps({'error': f'No recommendation found for topic: {topic}'})
        }

def get_all_recommendations():
    """
    Retorna as recomendações mais recentes para todos os tópicos.
    """
    all_recommendations = {}
    for topic in TOPICS:
        recommendation = get_latest_recommendation(topic)
        if recommendation['statusCode'] == 200:
            all_recommendations[topic] = json.loads(recommendation['body'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(all_recommendations)
    }

def generate_all_recommendations():
    """
    Gera recomendações para todos os tópicos.
    """
    results = {}
    for topic in TOPICS:
        result = generate_recommendation_for_topic(topic)
        results[topic] = json.loads(result['body'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }