import json
import random
import time
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import traceback
from decimal import Decimal
import urllib.parse
from datetime import timezone
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializa clientes do boto3
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data', endpoint_url=f"https://a3bw5rp1377npv-ats.iot.us-east-1.amazonaws.com")

# Constantes
TOPIC_NAME = 'agriculture/air/moisture'
AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME = 'AIAgriculturalAirMoistureRecommendations'
AIR_MOISTURE_AVERAGES_DATA_TABLE_NAME = 'AirMoistureAverages'

# Tópicos para recomendações
# TOPICS = [
#     "Necessidade de Irrigação",
#     "Índice de Estresse Hídrico",
#     "Prevenção de Doenças",
#     "Eficiência no Uso da Água",
#     "Análise de Retenção de Água do Solo",
#     "Previsão de Colheita",
#     "Planejamento de Plantio",
#     "Avaliação do Impacto das Chuvas",
#     "Modelagem de Crescimento das Plantas",
#     "Detecção de Zonas de Solo Deficiente"
# ]

def encode_string(s):
    return s.encode('utf-8').decode('utf-8')

# Função principal
def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, indent=2))

    if 'httpMethod' in event and 'path' in event:
        return handle_api_gateway_event(event)
    elif 'moisture' in event:
        return process_moisture_data(event)
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Requisição inválida'}),
        'headers': get_cors_headers()
    }

# Função para lidar com eventos da API Gateway
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
        'body': json.dumps({'error': 'Requisição inválida'}),
        'headers': get_cors_headers()
    }

# Função para obter a última leitura de temperatura do ar
def get_latest_moisture():
    try:
        table = dynamodb.Table(AIR_MOISTURE_AVERAGES_DATA_TABLE_NAME)
        
        response = table.scan(
            ProjectionExpression="#date, readings",
            ExpressionAttributeNames={"#date": "date"},
            Limit=1
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhum dado de temperatura do ar encontrado'}),
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
        
        moisture = latest_reading.get('moisture')
        status = latest_reading.get('status')
        timestamp = latest_reading.get('timestamp')
        
        if moisture is None or status is None or timestamp is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Dados de leitura incompletos'}),
                'headers': get_cors_headers()
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'moisture': float(moisture),
                'status': status,
                'timestamp': timestamp
            }),
            'headers': get_cors_headers()
        }
    except Exception as e:
        print(f"Erro ao obter a última leitura de temperatura do ar: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao obter a última leitura de temperatura do ar: {str(e)}"}),
            'headers': get_cors_headers()
        }

# Função para processar dados de temperatura do ar recebidos
def process_moisture_data(event):
    try:
        moisture = event['moisture']
        status = event['status']
        crops = event['crops']  # Coleta o array crops corretamente
        timestamp = datetime.now().isoformat()

        # Verifica se crops é uma lista
        if not isinstance(crops, list):
            raise ValueError("Crops deve ser uma lista de culturas.")

        store_moisture_data(moisture, status, timestamp)

        # Gera recomendações passando também as culturas (crops)
        recommendations_result = generate_agriculture_recommendations(moisture, status, crops)

        return recommendations_result
    except Exception as e:
        print(f"Erro ao processar dados de temperatura do ar: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Falha ao processar dados de temperatura do ar: {str(e)}"}),
            'headers': get_cors_headers()
        }

# Função para armazenar dados de temperatura do ar no DynamoDB
def store_moisture_data(moisture, status, timestamp):
    table = dynamodb.Table(AIR_MOISTURE_AVERAGES_DATA_TABLE_NAME)
    date = timestamp.split('T')[0]
    
    try:
        existing_readings = table.get_item(
            Key={'date': date},
            ProjectionExpression="readings",
        ).get('Item', {}).get('readings', [])
        
        if existing_readings:
            last_reading = existing_readings[-1]
            if last_reading['timestamp'] == timestamp:
                print(f"Leitura duplicada detectada para o timestamp {timestamp}. Ignorando armazenamento.")
                return

        # Armazena a nova leitura de temperatura do ar
        response = table.update_item(
            Key={'date': date},
            UpdateExpression="SET thing_name = :tn, readings = list_append(if_not_exists(readings, :empty_list), :r), last_update = :lu",
            ExpressionAttributeValues={
                ':tn': TOPIC_NAME,
                ':r': [{
                    'timestamp': timestamp,
                    'moisture': Decimal(str(moisture)),  # Mantemos o Decimal aqui para o DynamoDB
                    'status': status
                }],
                ':lu': timestamp,
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )
        
        print(f"Dados de temperatura do ar armazenados com sucesso para a data {date}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"A tabela {AIR_MOISTURE_AVERAGES_DATA_TABLE_NAME} não foi encontrada. Verifique o nome da tabela e a região.")
        elif error_code == 'ConditionalCheckFailedException':
            print(f"Erro de condição ao atualizar o item para a data {date}. Verifique as condições de atualização.")
        else:
            print(f"Erro ao armazenar dados de temperatura do ar: {str(e)}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao armazenar dados de temperatura do ar: {str(e)}")
        raise

def generate_agriculture_recommendations(moisture, status, crops):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Iniciando geração de recomendações")
    print(f"[{timestamp}] Parâmetros recebidos - Umidade do ar: {moisture}%, Status: {status}, Culturas: {crops}")

    crops_str = ", ".join(crops)
    print(f"[{timestamp}] Culturas para o prompt: {crops_str}")

    prompt = encode_string(f'''Human: Você é um especialista em agricultura. Forneça recomendações detalhadas para as próximas quatro semanas com base na umidade do ar e nas culturas plantadas. 
    Considere os seguintes dados:
    - Umidade atual do ar: {moisture}%
    - Status atual: {status}
    - Culturas plantadas: {crops_str}

    O plano deve incluir:
    1. Avaliação da necessidade de irrigação e sugestões de melhorias para eficiência no uso da água.
    2. Identificação do índice de estresse hídrico das plantas.
    3. Recomendações de novas culturas mais adequadas às condições de umidade do ar.
    4. Prevenção de doenças relacionadas à umidade excessiva ou baixa.

    Formate sua resposta como um dicionário JSON, onde as chaves são as semanas e os valores são recomendações específicas para cada semana.

    {{
        "Semana 1": {{
            "recomendações": "Recomendações específicas para a semana 1..."
        }},
        "Semana 2": {{
            "recomendações": "Recomendações específicas para a semana 2..."
        }},
        ...
    }}

    Human: Obrigado. Por favor, forneça apenas o dicionário JSON com as recomendações, sem incluir nenhum texto introdutório ou conclusivo.

    Assistant:''')
    
    print(f"[{timestamp}] Prompt preparado para envio ao Bedrock!")

    max_retries = 5
    base_delay = 1  # segundo
    for attempt in range(max_retries):
        try:
            print(f"[{timestamp}] Tentativa {attempt + 1} de {max_retries} para invocar o modelo Bedrock")
            response = bedrock.invoke_model(
                modelId="anthropic.claude-v2:1",
                body=json.dumps({
                    "prompt": prompt,
                    "max_tokens_to_sample": 3000,
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
            save_recommendations(recommendations, moisture, status, timestamp)

            # Codifica o JSON garantindo que caracteres especiais sejam tratados corretamente
            response_body = {
                'moisture': float(moisture),
                'status': status,
                'crops': crops,
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

def save_recommendations(recommendations, moisture, status, timestamp):
    table = dynamodb.Table(AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
    
    print(f"[{timestamp}] Iniciando salvamento das recomendações no DynamoDB")

    try:
        items = []
        for topic, recommendation in recommendations.items():
            item = {
                'M': {
                    'topic': {'S': topic},
                    'recommendation': {'S': recommendation},
                    'moisture': {'N': str(moisture)},
                    'status': {'S': status},
                    'timestamp': {'S': timestamp}
                }
            }
            items.append(item)

        # Criar o item principal
        main_item = {
            'date': timestamp.split('T')[0],  # Chave primária
            'topic_name': TOPIC_NAME,
            'last_update': timestamp,
            'recommendations': {'L': items}
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
        table = dynamodb.Table(AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        
        seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%d')
        
        response = table.scan(
            FilterExpression=Key('last_update').gte(seven_days_ago)
        )
        
        items = response.get('Items', [])
        logger.info(f"Número de itens recuperados do DynamoDB: {len(items)}")
        
        recommendations = {}
        
        for item in items:
            logger.debug(f"Processando item: {json.dumps(item, default=decimal_default)}")
            
            topic_name = item.get('topic_name')
            recommendations_list = item.get('recommendations', {}).get('L', [])
            last_update = item.get('last_update')
            
            if not all([topic_name, recommendations_list, last_update]):
                logger.warning(f"Item incompleto encontrado: {item}")
                continue
            
            latest_recommendation = None
            for rec in recommendations_list:
                rec_data = rec.get('M', {})
                if rec_data.get('topic', {}).get('S') == 'completion':
                    recommendation_text = rec_data.get('recommendation', {}).get('S')
                    if recommendation_text:
                        latest_recommendation = recommendation_text
                        break
            
            if latest_recommendation:
                if topic_name not in recommendations or last_update > recommendations[topic_name]['last_update']:
                    recommendations[topic_name] = {
                        'recommendation': latest_recommendation,
                        'last_update': last_update
                    }
        
        result = {topic: data['recommendation'] for topic, data in recommendations.items()}
        
        logger.info(f"Número de recomendações processadas: {len(result)}")
        logger.debug(f"Recomendações processadas: {json.dumps(result, default=decimal_default)}")
        
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

        table = dynamodb.Table(AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
        print(f"Nome da tabela DynamoDB: {AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME}")
        
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

# Função para obter a última recomendação por tópico
def get_latest_recommendation(topic):
    try:
        table = dynamodb.Table(AGRICULTURAL_AIR_MOISTURE_RECOMMENDATIONS_DYNAMODB_TABLE_NAME)
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
        
def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, ensure_ascii=False, default=str),
        'headers': get_cors_headers()
    }
    
# Função para obter cabeçalhos CORS
def get_cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
    }

# Função para obter o histórico de temperatura do ar
def get_moisture_history():
    try:
        table = dynamodb.Table(AIR_MOISTURE_AVERAGES_DATA_TABLE_NAME)
        
        # Definir o período de tempo para buscar o histórico (por exemplo, últimos 7 dias)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        response = table.query(
            KeyConditionExpression=Key('date').between(start_date.isoformat(), end_date.isoformat()),
            ScanIndexForward=False  # Para obter os resultados mais recentes primeiro
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Nenhum dado de histórico encontrado'}),
                'headers': get_cors_headers()
            }
        
        # Processar e formatar os dados do histórico
        history = []
        for item in items:
            date = item['date']
            readings = item.get('readings', [])
            for reading in readings:
                history.append({
                    'date': date,
                    'timestamp': reading['timestamp'],
                    'moisture': float(reading['moisture']),
                    'status': reading['status']
                })
        
        # Ordenar o histórico por timestamp
        history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            'statusCode': 200,
            'body': json.dumps(history),
            'headers': get_cors_headers()
        }
    except Exception as e:
        print(f"Erro ao obter o histórico de temperatura do ar: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao obter o histórico de temperatura do ar: {str(e)}"}),
            'headers': get_cors_headers()
        }