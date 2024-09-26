import json
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError
import uuid
import logging
import time
import re
from decimal import Decimal

# Configuração do logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialização dos clientes AWS
bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')

# Definição das tabelas DynamoDB
soil_moisture_task_plan_table = dynamodb.Table('AISoilMoistureTaskPlans')
soil_moisture_history_table = dynamodb.Table('SoilMoistureHistory')
soil_moisture_averages_table = dynamodb.Table('SoilMoistureAverages')

# Constantes
MAX_TOKENS = 2000
TEMPERATURE = 0.5
TOP_P = 0.9

# Custom JSON Encoder para lidar com objetos Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        if 'httpMethod' in event:
            if event['httpMethod'] == 'GET':
                # Verifica se o path termina com 'task-plan'
                if event.get('path', '').endswith('/task-plan'):
                    return get_all_task_plans()
                elif 'queryStringParameters' in event and event['queryStringParameters']:
                    return handle_get_request(event)
                else:
                    return create_response(400, "Parâmetros de consulta ausentes ou inválidos.")
            else:
                return create_response(405, "Método HTTP não permitido.")
        elif 'Records' in event:
            return handle_dynamodb_event(event['Records'])
        elif 'moisture' in event:
            logger.info("Processando dados de umidade do evento")
            return process_moisture_data(event)
        else:
            logger.info("Coletando dados de umidade do banco de dados")
            return handle_database_event()
    except Exception as e:
        logger.error(f"Erro no lambda_handler: {str(e)}")
        return create_response(500, f"Erro interno: {str(e)}")

def handle_get_request(event):
    query_params = event.get('queryStringParameters', {})
    if query_params and 'taskId' in query_params:
        return get_task_plan(query_params['taskId'])
    elif query_params and 'recommendations' in query_params:
        return get_recommendations(query_params['recommendations'])
    else:
        return create_response(400, "Parâmetros de consulta inválidos.")

def handle_dynamodb_event(records):
    for record in records:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            logger.info(f"Novo registro inserido na tabela SoilMoistureHistory: {json.dumps(new_image)}")
            return process_moisture_data(new_image)
    return create_response(200, "Eventos processados com sucesso.")

def handle_database_event():
    moisture_data = get_latest_moisture_from_averages()
    if not moisture_data:
        moisture_data = get_latest_moisture_from_history()
    
    if moisture_data:
        return process_moisture_data(moisture_data)
    else:
        logger.error("Não foi possível obter dados de umidade de nenhuma tabela")
        return create_response(404, "Dados de umidade não encontrados")

def get_latest_moisture_from_averages():
    try:
        logger.info("Obtendo a última umidade da tabela SoilMoistureAverages")
        response = soil_moisture_averages_table.scan(Limit=1)
        items = response.get('Items', [])
        if items:
            latest_item = items[0]
            return {
                'moisture': latest_item['averageMoisture'],
                'status': latest_item.get('status', 'unknown'),
                'timestamp': latest_item['timestamp']
            }
        return None
    except Exception as e:
        logger.error(f"Erro ao obter umidade da tabela SoilMoistureAverages: {str(e)}")
        return None

def get_latest_moisture_from_history():
    try:
        logger.info("Obtendo a última umidade da tabela SoilMoistureHistory")
        response = soil_moisture_history_table.scan(Limit=1)
        items = response.get('Items', [])
        if items:
            latest_item = items[0]
            return {
                'moisture': latest_item['averageMoisture'],
                'status': latest_item.get('status', 'unknown'),
                'timestamp': latest_item['timestamp']
            }
        return None
    except Exception as e:
        logger.error(f"Erro ao obter umidade da tabela SoilMoistureHistory: {str(e)}")
        return None

def get_task_plan(task_id):
    try:
        response = soil_moisture_task_plan_table.get_item(Key={'planId': task_id})
        item = response.get('Item')
        if item:
            return create_response(200, json.dumps(item, cls=DecimalEncoder), get_cors_headers())
        else:
            return create_response(404, "Plano de tarefas não encontrado", get_cors_headers())
    except Exception as e:
        logger.error(f"Erro ao obter plano de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter plano de tarefas: {str(e)}", get_cors_headers())

def get_all_task_plans():
    try:
        logger.info("Iniciando get_all_task_plans")
        response = soil_moisture_task_plan_table.scan()
        logger.info(f"Resposta do scan: {response}")
        items = response.get('Items', [])
        logger.info(f"Items recuperados: {items}")
        return create_response(200, json.dumps(items, cls=DecimalEncoder), get_cors_headers())
    except Exception as e:
        logger.error(f"Erro ao obter todos os planos de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter todos os planos de tarefas: {str(e)}", get_cors_headers())

def process_moisture_data(data):
    try:
        logger.info(f"Dados recebidos para processamento: {data}")
        
        data = normalize_input_data(data)
        
        moisture = data.get('moisture')
        status = data.get('status')
        
        logger.info(f"Dados normalizados: moisture={moisture}, status={status}")
        
        if not validate_moisture_data(moisture):
            return create_response(400, 'Dados de umidade inválidos ou ausentes')

        logger.info(f"Processando dados de umidade: moisture={moisture}, status={status}")
        
        new_plan = generate_task_plan_with_ai(moisture, status)
        if new_plan:
            plan_id = store_task_plan(new_plan, moisture, status)
            if plan_id:
                logger.info(f"Plano de tarefas armazenado com sucesso. ID: {plan_id}")
                return create_response(200, f'Novo plano de tarefas gerado e armazenado com ID: {plan_id}')
            else:
                logger.error("Falha ao armazenar o plano de tarefas")
                return create_response(500, 'Falha ao armazenar o plano de tarefas')
        else:
            logger.error("Falha ao gerar o plano de tarefas")
            return create_response(500, 'Falha ao gerar o plano de tarefas')
    
    except ValueError as ve:
        logger.error(f"Erro de validação: {str(ve)}")
        return create_response(400, f"Erro de validação: {str(ve)}")
    except Exception as e:
        logger.error(f"Erro ao processar dados de umidade: {str(e)}")
        return create_response(500, f"Erro ao processar dados de umidade: {str(e)}")

def normalize_input_data(data):
    if isinstance(data, str):
        logger.info("Dados recebidos como string. Convertendo para dicionário.")
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("Falha ao decodificar a string JSON")
    
    if not isinstance(data, dict):
        raise ValueError(f"Formato de dados inesperado: {type(data)}")
    
    return data

def validate_moisture_data(moisture):
    if moisture is None:
        logger.error("Dados de umidade ausentes")
        return False
    
    try:
        moisture_value = Decimal(str(moisture))
        if moisture_value < 0 or moisture_value > 100:
            logger.error(f"Valor de umidade fora do intervalo válido: {moisture_value}")
            return False
    except ValueError:
        logger.error(f"Valor de umidade não é um número válido: {moisture}")
        return False
    
    return True

def get_recommendations(topic):
    try:
        recommendation_prompt = f"""Forneça recomendações detalhadas para {topic} em uma fazenda, considerando práticas agrícolas modernas e sustentáveis."""
        
        prompt = "Human: " + recommendation_prompt + "\n\nAssistant:"
        
        logger.info("Enviando prompt para o modelo de IA para o auxílio recomendação das tarefas...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 300,
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
            })
        )
        
        response_body = json.loads(response['body'].read())
        recommendations = response_body['completion']
        return create_response(200, recommendations.strip())
    except Exception as e:
        logger.error(f"Erro ao obter recomendações para {topic}: {str(e)}")
        return create_response(500, f"Erro ao obter recomendações: {str(e)}")

def generate_task_plan_with_ai(moisture, status):
    timestamp = int(time.time())
    logger.info(f"[{timestamp}] Iniciando geração do plano de tarefas")
    logger.info(f"[{timestamp}] Parâmetros recebidos - Umidade: {moisture}%, Status: {status}")

    try:
        prompt = f'''Human: Com base em uma umidade do solo de {moisture}% e status '{status}', 
        gere um plano de tarefas para a fazenda. Considere práticas agrícolas modernas e 
        sustentáveis. Forneça uma lista de tarefas e recomendações específicas.

        Assistant:'''
        
        logger.info(f"[{timestamp}] Enviando prompt para o modelo de IA...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 300,
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "stop_sequences": ["Human:"]
            })
        )
        
        logger.info(f"[{timestamp}] Resposta recebida do modelo de IA")
        response_body = json.loads(response['body'].read())
        recommendations = response_body['completion'].strip()
        
        plan = {
            'planId': str(uuid.uuid4()),
            'moisture': Decimal(str(moisture)),
            'status': status,
            'recommendations': recommendations,
            'timestamp': timestamp,
            'createdAt': timestamp  # Adicionando o campo createdAt
        }
        logger.info(f"[{timestamp}] Plano de tarefas gerado: {plan}")
        return plan
    except Exception as e:
        logger.error(f"[{timestamp}] Erro ao gerar o plano de tarefas com IA: {str(e)}")
        return None

def store_task_plan(plan, moisture, status):
    timestamp = datetime.now(timezone.utc).isoformat()
    logger.info(f"[{timestamp}] Iniciando armazenamento do plano de tarefas de umidade")
    logger.info(f"[{timestamp}] Parâmetros recebidos - Umidade: {moisture}, Status: {status}")
    
    try:
        plan_id = str(uuid.uuid4())
        logger.info(f"[{timestamp}] UUID gerado para o plano: {plan_id}")
        
        logger.info(f"[{timestamp}] Convertendo umidade para Decimal")
        moisture_decimal = Decimal(str(moisture))
        logger.info(f"[{timestamp}] Umidade convertida: {moisture_decimal}")
        
        task_item = {
            'planId': plan_id,
            'plan': plan,
            'moisture': moisture_decimal,
            'status': status,
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        logger.info(f"[{timestamp}] Item do plano de tarefas criado")
        logger.debug(f"[{timestamp}] Detalhes do item: {json.dumps(task_item, default=str)}")
        
        logger.info(f"[{timestamp}] Iniciando operação de put_item no DynamoDB")
        response = soil_moisture_task_plan_table.put_item(Item=task_item)
        logger.info(f"[{timestamp}] Operação put_item concluída")
        logger.debug(f"[{timestamp}] Resposta do DynamoDB: {json.dumps(response, default=str)}")
        
        logger.info(f"[{timestamp}] Plano de tarefas de umidade armazenado com sucesso. ID: {plan_id}")
        return plan_id
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            logger.error(f"[{timestamp}] Erro de validação ao armazenar plano: {str(e)}")
            logger.error(f"[{timestamp}] Detalhes do item: {json.dumps(task_item, default=str)}")
        else:
            logger.error(f"[{timestamp}] Erro do cliente ao armazenar plano: {str(e)}")
        logger.exception("Detalhes do erro:")
        return None
    except Exception as e:
        logger.error(f"[{timestamp}] Erro inesperado ao armazenar plano de tarefas de umidade: {str(e)}")
        logger.exception("Detalhes do erro:")
        return None
    finally:
        logger.info(f"[{timestamp}] Finalizando operação de armazenamento do plano de tarefas de umidade")

def create_response(status_code, body, headers=None):
    response = {
        'statusCode': status_code,
        'body': body,
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    if headers:
        response['headers'].update(headers)
    return response

def get_cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }