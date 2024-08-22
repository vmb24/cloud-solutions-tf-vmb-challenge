import json
import boto3
from datetime import datetime

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot = boto3.client('iot-data')

IOT_THING_NAME = 'moisture_sensor'

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
            topic = json.loads(event['body']).get('topic')
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
        response = iot.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode())
        state = payload['state']['reported']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'moisture': state['moisture'],
                'state': state['state'],
                'timestamp': state['timestamp']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_recommendation_for_topic(topic):
    """
    Gera uma recomendação para um tópico específico usando o Amazon Bedrock.
    """
    if topic not in TOPICS:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid topic'})
        }

    moisture_data = get_latest_moisture()
    if moisture_data['statusCode'] != 200:
        return moisture_data

    moisture_info = json.loads(moisture_data['body'])
    current_moisture = moisture_info['moisture']
    current_state = moisture_info['state']
    timestamp = moisture_info['timestamp']

    prompt = f"""
    Você é um especialista em agricultura. Forneça uma recomendação detalhada para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Umidade atual do solo: {current_moisture}%
    - Estado atual: {current_state}

    Forneça uma recomendação prática e acionável para o seguinte tópico:
    {topic}

    A recomendação deve ser específica, detalhada e diretamente relacionada ao nível de umidade atual.
    """

    response = bedrock.invoke_model(
        modelId="anthropic.claude-v2",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 500,
            "temperature": 0.7,
            "top_p": 0.9,
        })
    )

    recommendation = json.loads(response['body'].read())['completion'].strip()

    store_recommendation(topic, recommendation, current_moisture, current_state, timestamp)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'topic': topic,
            'recommendation': recommendation,
            'moisture': current_moisture,
            'state': current_state,
            'timestamp': timestamp
        })
    }

def store_recommendation(topic, recommendation, moisture, state, timestamp):
    """
    Armazena a recomendação gerada na tabela específica do tópico.
    """
    table_name = f"Recommendation_{topic.replace(' ', '_')}"
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'timestamp': timestamp,
            'recommendation': recommendation,
            'moisture': moisture,
            'state': state,
            'thing_name': IOT_THING_NAME
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

    table_name = f"Recommendation_{topic.replace(' ', '_')}"
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression='thing_name = :tn',
        ExpressionAttributeValues={':tn': IOT_THING_NAME},
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