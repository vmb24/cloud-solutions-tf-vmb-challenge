import json
import boto3
from datetime import datetime, timezone
import uuid
import logging
import time
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data')

task_plan_table = dynamodb.Table('AISoilTemperatureTaskPlans')
temperature_history_table = dynamodb.Table('SoilTemperatureHistory')

IOT_THING_NAME = "agricultural_sensor"

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        if 'httpMethod' in event:
            if event['httpMethod'] == 'GET':
                return handle_get_request(event)
            else:
                return create_response(405, "Método HTTP não permitido.")
        elif 'Records' in event:
            return handle_dynamodb_event(event['Records'])
        elif 'temperature' in event:
            logger.info("Processando dados de temperatura do solo do evento")
            return process_temperature_data(event)
        else:
            logger.info("Coletando dados de temperatura do solo do IoT Core")
            return handle_iot_event()
    except Exception as e:
        logger.error(f"Erro no lambda_handler: {str(e)}")
        return create_response(500, f"Erro interno: {str(e)}")

def handle_get_request(event):
    path = event.get('path', '')
    query_params = event.get('queryStringParameters', {})
    
    if path.endswith('/task-plan'):
        return get_all_task_plans()
    
    if query_params:
        if 'taskId' in query_params:
            return get_task_plan(query_params['taskId'])
        elif 'recommendations' in query_params:
            return get_recommendations(query_params['recommendations'])
    
    return get_latest_task_plans()

def handle_dynamodb_event(records):
    for record in records:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            logger.info(f"Novo registro inserido na tabela SoilTemperatureHistory: {json.dumps(new_image)}")
            return process_temperature_data(new_image)
    return create_response(200, "Eventos processados com sucesso.")

def handle_iot_event():
    iot_data = get_latest_temperature()
    if iot_data['statusCode'] == 200:
        temperature_data = json.loads(iot_data['body'])
        return process_temperature_data(temperature_data)
    else:
        logger.error(f"Falha ao obter dados do IoT Core: {iot_data['body']}")
        return iot_data

def get_latest_temperature():
    try:
        logger.info(f"Tentando obter shadow para o dispositivo: {IOT_THING_NAME}")
        response = iot_client.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode())
        logger.info(f"Payload do shadow recebido: {payload}")
        state = payload['state']['reported']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'temperature': state['temperature'],
                'status': state['status'],
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        }
    except Exception as e:
        logger.error(f"Erro ao obter shadow do dispositivo: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Ocorreu um erro ao chamar a operação GetThingShadow: {str(e)}"})
        }

def get_task_plan(task_id):
    try:
        response = task_plan_table.get_item(Key={'planId': task_id})
        item = response.get('Item')
        if item:
            return create_response(200, json.dumps(item, cls=CustomJSONEncoder), get_cors_headers())
        else:
            return create_response(404, "Plano de tarefas não encontrado", get_cors_headers())
    except Exception as e:
        logger.error(f"Erro ao obter plano de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter plano de tarefas: {str(e)}", get_cors_headers())

def get_all_task_plans():
    try:
        response = task_plan_table.scan()
        items = response.get('Items', [])
        return create_response(200, json.dumps(items, cls=CustomJSONEncoder), get_cors_headers())
    except Exception as e:
        logger.error(f"Erro ao obter todos os planos de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter todos os planos de tarefas: {str(e)}", get_cors_headers())

def get_latest_task_plans():
    try:
        response = task_plan_table.scan()
        items = response.get('Items', [])
        latest_plans = sorted(items, key=lambda x: x['createdAt'], reverse=True)[:5]

        return create_response(200, json.dumps(latest_plans, cls=CustomJSONEncoder), get_cors_headers())
    except Exception as e:
        logger.error(f"Erro ao obter as últimas tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter as últimas tarefas: {str(e)}", get_cors_headers())

def process_temperature_data(data):
    try:
        logger.info(f"Dados recebidos para processamento: {data}")
        
        if isinstance(data, str):
            logger.info("Dados recebidos como string. Tentando converter para dicionário.")
            data = json.loads(data)
        
        if not isinstance(data, dict):
            logger.error(f"Formato de dados inesperado: {type(data)}")
            return create_response(400, 'Formato de dados inválido')
        
        temperature = data.get('temperature')
        status = data.get('status')
        
        if temperature is None:
            logger.error("Dados de temperatura ausentes")
            return create_response(400, 'Dados de temperatura ausentes')
        
        logger.info(f"Processando dados de temperatura: temperature={temperature}, status={status}")
        
        new_plan = generate_task_plan_with_ai(temperature, status)
        if new_plan:
            plan_id = store_task_plan(new_plan, temperature, status)
            if plan_id:
                logger.info("Sucesso ao armazenar o plano de tarefas")
            else:
                logger.error("Falha ao armazenar o plano de tarefas")
        else:
            logger.error("Falha ao gerar o plano de tarefas")
        
        return create_response(200, 'Novo plano de tarefas gerado e armazenado')
    except Exception as e:
        logger.error(f"Erro ao processar dados de temperatura: {str(e)}")
        return create_response(500, f"Erro ao processar dados de temperatura: {str(e)}")

def get_recommendations(topic):
    try:
        recommendation_prompt = f"""Forneça recomendações detalhadas para {topic} em uma fazenda, considerando a temperatura do solo e práticas agrícolas modernas e sustentáveis."""
        
        prompt = "Human: " + recommendation_prompt + "\n\nAssistant:"
        
        logger.info("Enviando prompt para o modelo de IA para o auxílio recomendação das tarefas...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 300,
                "temperature": 0.7,
                "top_p": 0.9,
            })
        )
        
        response_body = json.loads(response['body'].read())
        recommendations = response_body['completion']
        return create_response(200, recommendations.strip())
    except Exception as e:
        logger.error(f"Erro ao obter recomendações para {topic}: {str(e)}")
        return create_response(500, f"Não foi possível obter recomendações para {topic} devido a um erro.")

def generate_task_plan_with_ai(temperature, status):
    timestamp = time.time()
    logger.info(f"[{timestamp}] Iniciando geração do plano de tarefas")
    logger.info(f"[{timestamp}] Parâmetros recebidos - Temperatura: {temperature}°C, Status: {status}")
    
    try:
        topics = ["manejo do solo baseado na temperatura",
                  "plantio considerando a temperatura do solo",
                  "cuidados com as culturas baseados na temperatura do solo",
                  "irrigação baseada na temperatura do solo"]
        
        recommendations = {topic: get_recommendations(topic)['body'] for topic in topics}
        logger.info(f"[{timestamp}] Recomendações obtidas para todos os tópicos")
        
        task_plan_prompt = f'''Human:
        Com base nos seguintes dados de temperatura do solo e recomendações:
        Temperatura em Tempo Real: {temperature}°C

        Recomendações de Manejo do Solo:
        {recommendations["manejo do solo baseado na temperatura"]}

        Recomendações de Plantio:
        {recommendations["plantio considerando a temperatura do solo"]}

        Recomendações de Cuidados com as Culturas:
        {recommendations["cuidados com as culturas baseados na temperatura do solo"]}

        Recomendações de Irrigação:
        {recommendations["irrigação baseada na temperatura do solo"]}

        Gere um plano detalhado de tarefas para as próximas 4 semanas, incluindo:
        1. Atividades de manejo do solo baseadas na temperatura
        2. Datas e horários recomendados para plantio
        3. Cuidados específicos com as culturas considerando a temperatura do solo
        4. Recomendações de irrigação ajustadas às condições climáticas
        Assistant:'''
        
        logger.info(f"[{timestamp}] Enviando prompt para a IA para gerar plano de tarefas...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps({
                "prompt": task_plan_prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop_sequences": ["Human:"]
            })
        )
        
        response_body = json.loads(response['body'].read())
        task_plan = response_body['completion'].strip()
        logger.info(f"[{timestamp}] Plano de tarefas gerado com sucesso")
        return task_plan
    except Exception as e:
        logger.error(f"[{timestamp}] Erro ao gerar plano de tarefas com IA: {str(e)}")
        return None

def store_task_plan(new_plan, temperature, status):
    timestamp = datetime.now(timezone.utc).isoformat()
    logger.info(f"[{timestamp}] Iniciando armazenamento do plano de tarefas")
    logger.info(f"[{timestamp}] Parâmetros recebidos - Temperatura: {temperature}, Status: {status}")
    
    try:
        plan_id = str(uuid.uuid4())
        logger.info(f"[{timestamp}] UUID gerado para o plano: {plan_id}")
        
        logger.info(f"[{timestamp}] Convertendo temperatura para Decimal")
        temp_decimal = Decimal(str(temperature))
        logger.info(f"[{timestamp}] Temperatura convertida: {temp_decimal}")
        
        task_item = {
            'planId': plan_id,
            'plan': new_plan,
            'temperature': temp_decimal,
            'status': status,
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        logger.info(f"[{timestamp}] Item do plano de tarefas criado")
        logger.debug(f"[{timestamp}] Detalhes do item: {json.dumps(task_item, default=str)}")
        
        logger.info(f"[{timestamp}] Iniciando operação de put_item no DynamoDB")
        response = task_plan_table.put_item(Item=task_item)
        logger.info(f"[{timestamp}] Operação put_item concluída")
        logger.debug(f"[{timestamp}] Resposta do DynamoDB: {json.dumps(response, default=str)}")
        
        logger.info(f"[{timestamp}] Plano de tarefas armazenado com sucesso. ID: {plan_id}")
        return plan_id
    except Exception as e:
        logger.error(f"[{timestamp}] Erro ao armazenar plano de tarefas: {str(e)}")
        logger.exception("Detalhes do erro:")
        return None
    finally:
        logger.info(f"[{timestamp}] Finalizando operação de armazenamento do plano de tarefas")

def create_response(status_code, body, headers=None):
    response = {
        'statusCode': status_code,
        'body': body,
        'headers': headers or {'Content-Type': 'application/json'}
    }
    return response

def get_cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }