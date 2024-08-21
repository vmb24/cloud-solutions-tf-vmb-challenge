import json
import boto3
from datetime import datetime

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.client('dynamodb')
iot_data = boto3.client('iot-data')

def lambda_handler(event, context):
    # Extrai o método HTTP e o caminho da requisição do evento
    http_method = event['httpMethod']
    path = event['path']

    # Roteamento das requisições baseado no método HTTP e caminho
    if http_method == 'GET':
        if path == '/recommendations':
            return get_latest_recommendations()
        elif path == '/recommendations/by-topic':
            topic = event['queryStringParameters'].get('topic')
            return get_recommendations_by_topic(topic)
        elif path == '/moisture':
            return get_latest_moisture()
    elif http_method == 'POST':
        if path == '/generate-recommendations':
            return generate_new_recommendations()

    # Retorna 404 se nenhuma rota corresponder
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found'})
    }

def get_latest_recommendations():
    # Consulta o DynamoDB para obter as recomendações mais recentes
    response = dynamodb.query(
        TableName='RecommendationsByTopic',
        Limit=10,
        ScanIndexForward=False,
        KeyConditionExpression='#ts = :ts',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={':ts': {'S': 'latest'}}
    )
    
    if not response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No recommendations found'})
        }

    recommendations = {item['topic']['S']: item['recommendation']['S'] for item in response['Items']}
    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }

def get_recommendations_by_topic(topic):
    if not topic:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Topic parameter is required'})
        }

    # Consulta o DynamoDB para obter as recomendações mais recentes para o tópico específico
    response = dynamodb.query(
        TableName='RecommendationsByTopic',
        Limit=1,
        ScanIndexForward=False,
        KeyConditionExpression='topic = :topic',
        ExpressionAttributeValues={':topic': {'S': topic}}
    )
    
    if not response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': f'No recommendations found for topic: {topic}'})
        }

    recommendation = response['Items'][0]
    return {
        'statusCode': 200,
        'body': json.dumps({
            'topic': topic,
            'recommendation': recommendation['recommendation']['S'],
            'timestamp': recommendation['timestamp']['S'],
            'averageMoisture': float(recommendation['averageMoisture']['N']),
            'state': recommendation['state']['S']
        })
    }

def get_latest_moisture():
    # Consulta o DynamoDB para obter a umidade média mais recente
    response = dynamodb.query(
        TableName='AverageMoisture',
        Limit=1,
        ScanIndexForward=False,
        KeyConditionExpression='#ts = :ts',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={':ts': {'S': 'latest'}}
    )
    
    if not response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No moisture data found'})
        }

    moisture_data = response['Items'][0]
    return {
        'statusCode': 200,
        'body': json.dumps({
            'averageMoisture': float(moisture_data['averageMoisture']['N']),
            'timestamp': moisture_data['timestamp']['S']
        })
    }

def generate_new_recommendations():
    # Obter dados do IoT Core
    response = iot_data.get_thing_shadow(
        thingName='humidity_sensor'
    )
    
    payload = json.loads(response['payload'].read())
    state = payload['state']['reported']

    average_moisture = state['averageMoisture']
    current_state = state.get('state', 'unknown')

    # Gerar recomendações usando Bedrock
    recommendations = generate_recommendations(average_moisture, current_state)

    # Armazenar dados nas tabelas do DynamoDB
    store_recommendations_by_topic(current_state, average_moisture, recommendations)
    store_moisture_by_state(current_state, average_moisture)
    store_average_moisture(average_moisture)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'averageMoisture': average_moisture,
            'state': current_state,
            'recommendations': recommendations
        })
    }


def generate_recommendations(moisture, state):
    prompt = f"""
    Você é um especialista em agricultura. Forneça recomendações detalhadas para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Umidade atual do solo: {moisture}%
    - Estado atual: {state}

    Forneça recomendações práticas e acionáveis para cada tópico a seguir. Separe cada tópico com o prefixo "TÓPICO:" seguido do nome do tópico em maiúsculas, e termine cada tópico com "FIM DO TÓPICO".

    1. Necessidade de Irrigação
    2. Índice de Estresse Hídrico
    3. Prevenção de Doenças
    4. Eficiência no Uso da Água
    5. Análise de Retenção de Água do Solo
    6. Previsão de Colheita
    7. Planejamento de Plantio
    8. Avaliação do Impacto das Chuvas
    9. Modelagem de Crescimento das Plantas
    10. Detecção de Zonas de Solo Deficiente
    """

    response = bedrock.invoke_model(
        modelId='ai21.j2-mid-v1',
        body=json.dumps({
            "prompt": prompt,
            "maxTokens": 2000,
            "temperature": 0.7,
            "topP": 1,
            "stopSequences": [],
            "countPenalty": {"scale": 0},
            "presencePenalty": {"scale": 0},
            "frequencyPenalty": {"scale": 0}
        })
    )

    bedrock_response = json.loads(response['body'].read())
    recommendations_text = bedrock_response['completions'][0]['data']['text']
    
    # Separar as recomendações por tópico
    topics = recommendations_text.split("TÓPICO:")[1:]  # Ignorar o texto antes do primeiro tópico
    recommendations = {}
    for topic in topics:
        topic_name, content = topic.split("\n", 1)
        content = content.strip().replace("FIM DO TÓPICO", "").strip()
        recommendations[topic_name.strip()] = content

    return recommendations

def store_recommendations_by_topic(state, moisture, recommendations):
    timestamp = datetime.now().isoformat()
    for topic, recommendation in recommendations.items():
        dynamodb.put_item(
            TableName='RecommendationsByTopic',
            Item={
                'state': {'S': state},
                'topic': {'S': topic},
                'timestamp': {'S': timestamp},
                'averageMoisture': {'N': str(moisture)},
                'recommendation': {'S': recommendation}
            }
        )

def store_moisture_by_state(state, moisture):
    timestamp = datetime.now().isoformat()
    dynamodb.put_item(
        TableName='MoistureByState',
        Item={
            'state': {'S': state},
            'timestamp': {'S': timestamp},
            'averageMoisture': {'N': str(moisture)}
        }
    )

def store_average_moisture(moisture):
    timestamp = datetime.now().isoformat()
    dynamodb.put_item(
        TableName='AverageMoisture',
        Item={
            'timestamp': {'S': timestamp},
            'averageMoisture': {'N': str(moisture)}
        }
    )