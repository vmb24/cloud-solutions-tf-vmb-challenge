import json
import random
import time
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

IOT_THING_NAME = 'luminosity_sensor'
AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME = 'AIAgriculturalLuminosityRecommendations'
LUMINOSITY_AVERAGES_DATA_TABLE_NAME = 'LuminosityAverages'

TOPICS = [
    "Gerenciamento de Culturas",
    "Fotossíntese e Crescimento",
    "Floração e Polinização",
    "Maturação e Colheita",
    "Manejo de Sombra",
    "Eficiência Energética",
    "Qualidade da Produção",
    "Ciclo Circadiano das Plantas",
    "Controle de Pragas e Doenças",
    "Planejamento de Plantio"
]

def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, indent=2))

    if 'httpMethod' in event and 'path' in event:
        return handle_api_gateway_event(event)
    elif 'luminosity' in event:
        return process_luminosity_data(event)
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Requisição inválida'}),
        'headers': get_cors_headers()
    }

def handle_api_gateway_event(event):
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'GET':
        if path == '/luminosity':
            return get_latest_luminosity()
        elif path == '/luminosity/history':
            return get_luminosity_history()
        elif path == '/recommendations':
            return get_all_recommendations()
        elif path.startswith('/recommendation/'):
            topic = path.split('/')[-1]
            return get_latest_recommendation(topic)

    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Requisição inválida'}),
        'headers': get_cors_headers()
    }

def get_latest_luminosity():
    try:
        table = dynamodb.Table(LUMINOSITY_AVERAGES_DATA_TABLE_NAME)
        
        response = table.scan(
            ProjectionExpression="#date, readings",
            ExpressionAttributeNames={"#date": "date"},
            Limit=1,
            ScanIndexForward=False
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhum dado de luminosidade encontrado'}),
                'headers': get_cors_headers()
            }
        
        latest_item = items[0]
        readings = latest_item.get('readings', [])
        
        if not readings:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhuma leitura encontrada para o último registro'}),
                'headers': get_cors_headers()
            }
        
        latest_reading = readings[-1]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'luminosity': float(latest_reading['luminosity']),
                'status': latest_reading['status'],
                'timestamp': latest_reading['timestamp']
            }),
            'headers': get_cors_headers()
        }
    except Exception as e:
        print(f"Erro ao obter a última leitura de luminosidade: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao obter a última leitura de luminosidade: {str(e)}"}),
            'headers': get_cors_headers()
        }

def process_luminosity_data(event):
    try:
        luminosity = event['luminosity']
        status = event['status']
        timestamp = datetime.now().isoformat()

        store_luminosity_data(luminosity, status, timestamp)

        recommendations_result = generate_all_recommendations(luminosity, status)

        return recommendations_result
    except Exception as e:
        print(f"Erro ao processar dados de luminosidade: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Falha ao processar dados de luminosidade: {str(e)}"}),
            'headers': get_cors_headers()
        }

def store_luminosity_data(luminosity, status, timestamp):
    table = dynamodb.Table(LUMINOSITY_AVERAGES_DATA_TABLE_NAME)
    date = timestamp.split('T')[0]
    
    try:
        response = table.update_item(
            Key={'date': date},
            UpdateExpression="SET thing_name = :tn, readings = list_append(if_not_exists(readings, :empty_list), :r), last_update = :lu",
            ExpressionAttributeValues={
                ':tn': IOT_THING_NAME,
                ':r': [{
                    'timestamp': timestamp,
                    'luminosity': Decimal(str(luminosity)),
                    'status': status
                }],
                ':lu': timestamp,
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )
        
        if response.get('Attributes', {}).get('readings', []):
            print(f"Dados de luminosidade atualizados para a data {date}")
        else:
            print(f"Novo item criado para a data {date}")
        
        print(f"Dados de luminosidade armazenados com sucesso para a data {date}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"A tabela {LUMINOSITY_AVERAGES_DATA_TABLE_NAME} não foi encontrada. Verifique o nome da tabela e a região.")
        elif error_code == 'ConditionalCheckFailedException':
            print(f"Erro de condição ao atualizar o item para a data {date}. Verifique as condições de atualização.")
        else:
            print(f"Erro ao armazenar dados de luminosidade: {str(e)}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao armazenar dados de luminosidade: {str(e)}")
        raise

def get_luminosity_history(days=30):
    table = dynamodb.Table(LUMINOSITY_AVERAGES_DATA_TABLE_NAME)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    response = table.scan(
        FilterExpression=Key('date').between(start_date.isoformat(), end_date.isoformat())
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items']),
        'headers': get_cors_headers()
    }

def generate_all_recommendations(luminosity, status):
    timestamp = datetime.now().isoformat()
    
    print(f"Gerando recomendações para todos os tópicos. Luminosidade: {luminosity}, Status: {status}")
    
    topics_prompt = "\n".join([f"- {topic}" for topic in TOPICS])
    
    prompt = f'''Human: Você é um especialista em agricultura. Forneça recomendações detalhadas para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Luminosidade atual: {luminosity} lux
    - Status atual: {status}

    Forneça uma recomendação prática e acionável para cada um dos seguintes tópicos:
    {topics_prompt}

    Cada recomendação deve ser específica, detalhada e diretamente relacionada ao nível de luminosidade atual. Responda em português.
    Formate sua resposta como um dicionário JSON, onde a chave é o tópico e o valor é a recomendação correspondente.

    Assistant: Aqui está um dicionário JSON com recomendações para cada tópico baseado nos dados fornecidos:

    {{
        "Gerenciamento de Culturas": "Recomendação para Gerenciamento de Culturas...",
        "Fotossíntese e Crescimento": "Recomendação para Fotossíntese e Crescimento...",
        ...
    }}

    Human: Obrigado. Por favor, forneça apenas o dicionário JSON com as recomendações, sem incluir nenhum texto introdutório ou conclusivo.
    
    Assistant:'''

    print(f"Enviando requisição para o Bedrock com o prompt para todos os tópicos")
    
    max_retries = 5
    base_delay = 1  # segundo
    for attempt in range(max_retries):
        try:
            response = bedrock.invoke_model(
                modelId="anthropic.claude-v2",
                body=json.dumps({
                    "prompt": prompt,
                    "max_tokens_to_sample": 3000,
                    "temperature": 0.5,
                    "top_p": 1,
                    "stop_sequences": ["\n\nHuman:"]
                })
            )
            print(f"Resposta do Bedrock recebida com sucesso")
            break
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt == max_retries - 1:
                    print(f"Erro ao chamar o Bedrock após {max_retries} tentativas: {str(e)}")
                    return {
                        'statusCode': 500,
                        'body': json.dumps({'error': f'Falha ao gerar recomendações após {max_retries} tentativas: {str(e)}'}),
                        'headers': get_cors_headers()
                    }
                delay = (2 ** attempt * base_delay) + (random.randint(0, 1000) / 1000.0)
                print(f"Throttling detectado. Tentativa {attempt + 1} de {max_retries}. Aguardando {delay:.2f} segundos.")
                time.sleep(delay)
            else:
                raise
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao gerar recomendações após {max_retries} tentativas'}),
            'headers': get_cors_headers()
        }

    recommendations = json.loads(response['body'].read())['completion'].strip()
    print(f"Recomendações geradas: {recommendations}")

    try:
        recommendations_dict = json.loads(recommendations)
    except json.JSONDecodeError:
        print("Erro ao decodificar as recomendações como JSON")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Falha ao decodificar as recomendações como JSON'}),
            'headers': get_cors_headers()
        }

    try:
        store_recommendation(recommendations_dict, luminosity, status, timestamp)
        print("Todas as recomendações armazenadas com sucesso")
    except Exception as e:
        print(f"Erro ao armazenar recomendações: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao armazenar recomendações: {str(e)}'}),
            'headers': get_cors_headers()
        }

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations_dict),
        'headers': get_cors_headers()
    }

def store_recommendation(recommendations_dict, luminosity, status, timestamp):
    try:
        print("Tentando armazenar recomendações")
        print(f"Nome da tabela DynamoDB: {AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME}")
        
        table = dynamodb.Table(AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        date = timestamp.split('T')[0]
        
        recommendations = []
        for topic, recommendation in recommendations_dict.items():
            recommendations.append({
                'topic': topic,
                'recommendation': recommendation,
                'luminosity': Decimal(str(luminosity)),
                'status': status,
                'timestamp': timestamp
            })
        
        response = table.update_item(
            Key={'date': date},
            UpdateExpression="SET thing_name = :tn, recommendations = list_append(if_not_exists(recommendations, :empty_list), :r), last_update = :lu",
            ExpressionAttributeValues={
                ':tn': IOT_THING_NAME,
                ':r': recommendations,
                ':lu': timestamp,
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )
        
        if response.get('Attributes', {}).get('recommendations', []):
            print(f"Recomendações atualizadas para a data {date}")
        else:
            print(f"Novo item de recomendações criado para a data {date}")
        
        print(f"Recomendações armazenadas com sucesso para a data {date}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"A tabela {AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME} não foi encontrada. Verifique o nome da tabela e a região.")
        elif error_code == 'ConditionalCheckFailedException':
            print(f"Erro de condição ao atualizar o item para a data {date}. Verifique as condições de atualização.")
        else:
            print(f"Erro ao armazenar recomendações: {str(e)}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao armazenar recomendações: {str(e)}")
        raise

def get_all_recommendations():
    table = dynamodb.Table(AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
    response = table.scan()
    recommendations = []
    for item in response['Items']:
        recommendations.extend(item.get('recommendations', []))
    return {
        'statusCode': 200,
        'body': json.dumps(recommendations),
        'headers': get_cors_headers()
    }

def get_latest_recommendation(topic):
    table = dynamodb.Table(AGRICULTURAL_LUMINOSITY_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
    response = table.scan(
        ProjectionExpression="recommendations",
        FilterExpression="contains(recommendations, :topic)",
        ExpressionAttributeValues={':topic': topic}
    )
    
    all_recommendations = []
    for item in response['Items']:
        all_recommendations.extend(item.get('recommendations', []))
    
    topic_recommendations = [r for r in all_recommendations if r['topic'] == topic]
    topic_recommendations.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if topic_recommendations:
        return {
            'statusCode': 200,
            'body': json.dumps(topic_recommendations[0]),
            'headers': get_cors_headers()
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Recomendação não encontrada'}),
            'headers': get_cors_headers()
        }

def get_cors_headers():
    return {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }