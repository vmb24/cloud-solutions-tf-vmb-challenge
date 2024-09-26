import json
import random
import time
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal
import urllib.parse
import traceback
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialização dos clientes
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

# Constantes
TOPIC_NAME = 'agriculture/soil/temperature'
AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME = 'AIAgriculturalSoilTemperatureRecommendations'
SOIL_TEMPERATURE_AVERAGES_DATA_TABLE_NAME = 'SoilTemperatureAverages'
TOPICS = [
    "Gerenciamento de Estresse Térmico",
    "Otimização de Irrigação",
    "Proteção contra Geadas",
    "Manejo de Culturas em Altas Temperaturas",
    "Ajuste de Cronograma de Plantio",
    "Ventilação e Sombreamento",
    "Monitoramento de Doenças Relacionadas à Temperatura",
    "Eficiência Energética em Estufas",
    "Adaptação de Variedades de Culturas",
    "Práticas de Conservação do Solo"
]

def encode_string(s):
    return s.encode('utf-8').decode('utf-8')

def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, indent=2, default=str))

    if 'httpMethod' in event and 'path' in event:
        return handle_api_gateway_event(event)
    elif 'temperature' in event:
        return process_temperature_data(event)
    
    return create_response(400, {'error': 'Requisição inválida'})

def handle_api_gateway_event(event):
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'GET':
        if path == '/temperature':
            return get_latest_temperature()
        elif path == '/temperature/history':
            return get_temperature_history()
        elif path == '/recommendations':
            return get_all_recommendations()
        elif path == '/recommendations/by-topic':
            return get_recommendations_by_topic(event)
        elif path.startswith('/recommendation/'):
            topic = path.split('/')[-1]
            return get_latest_recommendation(topic)

    return create_response(400, {'error': 'Requisição inválida'})

def get_latest_temperature():
    try:
        table = dynamodb.Table(SOIL_TEMPERATURE_AVERAGES_DATA_TABLE_NAME)
        
        response = table.scan(
            ProjectionExpression="#date, readings",
            ExpressionAttributeNames={"#date": "date"},
            Limit=1
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhum dado de umidade encontrado'}),
                'headers': get_cors_headers()
            }
        
        latest_item = max(items, key=lambda x: x['date'])
        readings = latest_item.get('readings', [])
        
        if not readings or not isinstance(readings, list):
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhuma leitura encontrada para o último registro ou formato inválido'}),
                'headers': get_cors_headers()
            }
        
        latest_reading = max(readings, key=lambda x: x.get('timestamp', ''))
        
        if not isinstance(latest_reading, dict):
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Formato de leitura inválido'}),
                'headers': get_cors_headers()
            }
        
        temperature = latest_reading.get('temperature')
        status = latest_reading.get('status')
        timestamp = latest_reading.get('timestamp')
        
        if temperature is None or status is None or timestamp is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Dados de leitura incompletos'}),
                'headers': get_cors_headers()
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'temperature': float(temperature),
                'status': status,
                'timestamp': timestamp
            }),
            'headers': get_cors_headers()
        }
    except Exception as e:
        print(f"Erro ao obter a última leitura de umidade: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao obter a última leitura de umidade: {str(e)}"}),
            'headers': get_cors_headers()
        }

def process_temperature_data(event):
    try:
        temperature = event['temperature']
        status = event['status']
        timestamp = datetime.now().isoformat()

        store_temperature_data(temperature, status, timestamp)
        recommendations_result = generate_all_recommendations(temperature, status)

        return recommendations_result
    except Exception as e:
        print(f"Erro ao processar dados de temperatura: {str(e)}")
        return create_response(500, {'error': f"Falha ao processar dados de temperatura: {str(e)}"})

def store_temperature_data(temperature, status, timestamp):
    table = dynamodb.Table(SOIL_TEMPERATURE_AVERAGES_DATA_TABLE_NAME)
    date = timestamp.split('T')[0]
    
    try:
        response = table.update_item(
            Key={'date': date},
            UpdateExpression="SET thing_name = :tn, readings = list_append(if_not_exists(readings, :empty_list), :r), last_update = :lu",
            ExpressionAttributeValues={
                ':tn': TOPIC_NAME,
                ':r': [{
                    'timestamp': timestamp,
                    'temperature': Decimal(str(temperature)),
                    'status': status
                }],
                ':lu': timestamp,
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )
        
        if response.get('Attributes', {}).get('readings', []):
            print(f"Dados de temperatura atualizados para a data {date}")
        else:
            print(f"Novo item criado para a data {date}")
        
        print(f"Dados de temperatura armazenados com sucesso para a data {date}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"A tabela {SOIL_TEMPERATURE_AVERAGES_DATA_TABLE_NAME} não foi encontrada. Verifique o nome da tabela e a região.")
        elif error_code == 'ConditionalCheckFailedException':
            print(f"Erro de condição ao atualizar o item para a data {date}. Verifique as condições de atualização.")
        else:
            print(f"Erro ao armazenar dados de temperatura: {str(e)}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao armazenar dados de temperatura: {str(e)}")
        raise

def get_temperature_history(days=30):
    try:
        table = dynamodb.Table(SOIL_TEMPERATURE_AVERAGES_DATA_TABLE_NAME)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        response = table.scan(
            FilterExpression=Key('date').between(start_date.isoformat(), end_date.isoformat())
        )

        return create_response(200, response['Items'])
    except Exception as e:
        print(f"Erro ao obter histórico de temperatura: {str(e)}")
        return create_response(500, {'error': f"Falha ao obter histórico de temperatura: {str(e)}"})
    
def get_latest_recommendation(topic):
    try:
        table = dynamodb.Table(AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        response = table.query(
            KeyConditionExpression=Key('topic').eq(topic),
            ScanIndexForward=False,
            Limit=1
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'Nenhuma recomendação encontrada para o tópico: {topic}'}),
                'headers': get_cors_headers()
            }
        
        latest_recommendation = items[0]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'topic': topic,
                'recommendation': latest_recommendation['recommendation'],
                'timestamp': latest_recommendation['timestamp']
            }),
            'headers': get_cors_headers()
        }
    except Exception as e:
        print(f"Erro ao obter a última recomendação para {topic}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao obter a recomendação para {topic}: {str(e)}'}),
            'headers': get_cors_headers()
        }

def generate_all_recommendations(temperature, status):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Iniciando geração de recomendações")
    print(f"[{timestamp}] Parâmetros recebidos - Temperatura: {temperature}%, Status: {status}")

    topics_prompt = "\n".join([f"- {encode_string(topic)}" for topic in TOPICS])
    print(f"[{timestamp}] Tópicos preparados: {topics_prompt}")

    prompt = encode_string(f'''Human: Você é um especialista em agricultura. Forneça recomendações detalhadas para otimizar a saúde e produção das plantas com base nos seguintes dados:
    - Temperatura atual: {temperature}°C
    - Status atual: {status}

    Forneça uma recomendação prática e acionável para cada um dos seguintes tópicos:
    {topics_prompt}

    Cada recomendação deve ser específica, detalhada e diretamente relacionada à temperatura atual. Responda em português.
    Formate sua resposta como um dicionário JSON, onde a chave é o tópico e o valor é a recomendação correspondente.

    Assistant: Aqui está um dicionário JSON com recomendações para cada tópico baseado nos dados fornecidos:

    {{
        "Gerenciamento de Estresse Térmico": "Recomendação para Gerenciamento de Estresse Térmico...",
        "Otimização de Irrigação": "Recomendação para Otimização de Irrigação...",
        ...
    }}

    Human: Obrigado. Por favor, forneça apenas o dicionário JSON com as recomendações, sem incluir nenhum texto introdutório ou conclusivo.

    Assistant:''')

    print(f"[{timestamp}] Prompt preparado para envio ao Bedrock")

    max_retries = 5
    base_delay = 1  # segundo
    for attempt in range(max_retries):
        try:
            print(f"[{timestamp}] Tentativa {attempt + 1} de {max_retries} para invocar o modelo Bedrock")
            response = bedrock.invoke_model(
                modelId="anthropic.claude-v2",
                body=json.dumps({
                    "prompt": prompt,
                    "max_tokens_to_sample": 3000,
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "stop_sequences": ["Human:"]
                }),
                contentType="application/json"
            )
            print(f"[{timestamp}] Resposta recebida do Bedrock")
            
            result = json.loads(response['body'].read().decode('utf-8'))
            print(f"[{timestamp}] Resposta decodificada: {result}")

            # Verifica se result contém as recomendações
            recommendations = {encode_string(key): encode_string(value) for key, value in result.items() if isinstance(value, str)}
            print(f"[{timestamp}] Recomendações extraídas: {recommendations}")

            # Converte Decimal para float antes de retornar
            recommendations = {topic: float(rec) if isinstance(rec, Decimal) else rec for topic, rec in recommendations.items()}
            print(f"[{timestamp}] Recomendações processadas: {recommendations}")

            # Salva as recomendações no DynamoDB
            save_recommendations(recommendations, temperature, status, timestamp)

            # Codifica o JSON garantindo que caracteres especiais sejam tratados corretamente
            response_body = {
                'temperature': float(temperature),
                'status': status,
                'recommendations': recommendations,
                'timestamp': timestamp
            }
            print(f"[{timestamp}] Corpo da resposta preparado: {response_body}")

            return {
                'statusCode': 200,
                'body': json.dumps(response_body, ensure_ascii=False),
                'headers': get_cors_headers()
            }
        except ClientError as e:
            print(f"[{timestamp}] Erro do cliente Bedrock (Tentativa {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"[{timestamp}] Aguardando {delay} segundos antes da próxima tentativa")
                time.sleep(delay)
            else:
                print(f"[{timestamp}] Todas as tentativas falharam")
                raise
        except json.JSONDecodeError as e:
            print(f"[{timestamp}] Erro ao decodificar JSON da resposta do Bedrock: {str(e)}")
            raise
        except Exception as e:
            print(f"[{timestamp}] Erro inesperado na chamada ao Bedrock: {str(e)}")
            raise

    print(f"[{timestamp}] Retornando resposta de erro após falhas múltiplas")
    return {
        'statusCode': 500,
        'body': json.dumps({'error': 'Falha ao gerar recomendações'}, ensure_ascii=False),
        'headers': get_cors_headers()
    }

def save_recommendations(recommendations, temperature, status, timestamp):
    table = dynamodb.Table(AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
    
    print(f"[{timestamp}] Iniciando salvamento das recomendações no DynamoDB")

    try:
        items = []
        for topic, recommendation in recommendations.items():
            item = {
                'topic': topic,
                'recommendation': recommendation,
                'temperature': str(temperature),
                'status': status,
                'timestamp': timestamp
            }
            items.append(item)

        # Criar o item principal
        main_item = {
            'date': timestamp.split('T')[0],  # Chave primária
            'topic_name': TOPIC_NAME,
            'last_update': timestamp,
            'recommendations': items
        }

        response = table.put_item(Item=main_item)
        print(f"[{timestamp}] Recomendações salvas com sucesso. Resposta do DynamoDB: {response}")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"[{timestamp}] Erro ao salvar recomendações. Código de erro: {error_code}, Mensagem: {error_message}")
        raise
    except Exception as e:
        print(f"[{timestamp}] Erro inesperado ao salvar recomendações: {str(e)}")
        raise

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_all_recommendations():
    try:
        logger.info("Iniciando a obtenção de todas as recomendações")
        table = dynamodb.Table(AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        response = table.scan()
        
        items = response.get('Items', [])
        logger.info(f"Itens recuperados do DynamoDB: {json.dumps(items, default=decimal_default)}")
        
        recommendations = {}
        
        for item in items:
            if not isinstance(item, dict):
                logger.warning(f"Item inesperado encontrado: {item}")
                continue
            
            recommendations_list = item.get('recommendations', [])
            
            if not isinstance(recommendations_list, list):
                logger.warning(f"recommendations não é uma lista: {recommendations_list}")
                continue
            
            for rec in recommendations_list:
                if not isinstance(rec, dict):
                    logger.warning(f"Recomendação inválida encontrada: {rec}")
                    continue
                
                topic = rec.get('topic', '')
                recommendation_text = rec.get('recommendation', '')
                timestamp = rec.get('timestamp', '')
                
                if not all([topic, recommendation_text, timestamp]):
                    logger.warning(f"Recomendação incompleta encontrada: {rec}")
                    continue
                
                if topic not in recommendations or timestamp > recommendations[topic]['timestamp']:
                    recommendations[topic] = {
                        'recommendation': recommendation_text,
                        'timestamp': timestamp
                    }
        
        result = {topic: data['recommendation'] for topic, data in recommendations.items()}
        
        logger.info(f"Recomendações processadas: {json.dumps(result, default=decimal_default)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result, default=decimal_default),
            'headers': get_cors_headers()
        }
    except Exception as e:
        logger.error(f"Erro ao obter recomendações: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Falha ao obter recomendações: {str(e)}'}, default=decimal_default),
            'headers': get_cors_headers()
        }

def get_recommendations_by_topic(event):
    try:
        print(f"Evento recebido: {json.dumps(event)}")  # Log do evento completo
        
        encoded_topic = event.get('queryStringParameters', {}).get('topic')
        print(f"Tópico codificado: {encoded_topic}")  # Log do tópico codificado
        
        if not encoded_topic:
            error_response = create_response(400, {'error': 'O parâmetro "topic" é obrigatório'})
            print(f"Resposta de erro 400: {json.dumps(error_response)}")
            return error_response

        # Tente decodificar o tópico de várias maneiras
        topic_utf8 = urllib.parse.unquote(encoded_topic)
        topic_latin1 = urllib.parse.unquote(encoded_topic, encoding='latin-1')
        topic_raw = encoded_topic.replace('\\u00e7', 'ç').replace('\\u00e3', 'ã')

        print(f"Tópico decodificado UTF-8: {topic_utf8}")
        print(f"Tópico decodificado Latin-1: {topic_latin1}")
        print(f"Tópico decodificado Raw: {topic_raw}")

        # Use o tópico raw para a consulta
        topic = topic_raw

        table = dynamodb.Table(AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        print(f"Nome da tabela DynamoDB: {AGRICULTURAL_SOIL_TEMPERATURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME}")
        
        response = table.query(
            KeyConditionExpression=Key('topic').eq(topic),
            ScanIndexForward=False
        )
        print(f"Resposta do DynamoDB: {json.dumps(response, default=str)}")
        
        items = response.get('Items', [])

        if not items:
            error_response = create_response(404, {'error': f'Nenhuma recomendação encontrada para o tópico: {topic}'})
            print(f"Resposta de erro 404: {json.dumps(error_response)}")
            return error_response

        formatted_items = [{
            'topic': item['topic'],
            'recommendation': item['recommendation'],
            'timestamp': item['timestamp']
        } for item in items]

        success_response = create_response(200, {
            'topic': topic,
            'recommendations': formatted_items
        })
        print(f"Resposta de sucesso 200: {json.dumps(success_response)}")
        return success_response

    except Exception as e:
        error_message = f"Falha ao obter recomendações por tópico: {str(e)}"
        error_response = create_response(500, {'error': error_message})
        print(f"Resposta de erro 500: {json.dumps(error_response)}")
        print(f"Traceback: {traceback.format_exc()}")
        return error_response

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, ensure_ascii=False, default=str),
        'headers': get_cors_headers()
    }

def get_cors_headers():
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }