import json
import boto3
from datetime import datetime, timezone
import uuid
import logging
import time
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')
iot_client = boto3.client('iot-data')

task_plan_table = dynamodb.Table('SoilTemperatureTaskPlans')
temperature_history_table = dynamodb.Table('SoilTemperatureHistory')

IOT_THING_NAME = "soil_temperature_sensor"

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        if event['httpMethod'] == 'GET':
            if 'taskId' in event['queryStringParameters']:
                return get_task_plan(event['queryStringParameters']['taskId'])
            elif 'recommendations' in event['queryStringParameters']:
                return get_recommendations(event['queryStringParameters']['recommendations'])
            else:
                return get_all_task_plans()
        elif 'Records' in event:
            for record in event['Records']:
                if record['eventName'] == 'INSERT':
                    new_image = record['dynamodb']['NewImage']
                    logger.info(f"Novo registro inserido na tabela SoilTemperatureHistory: {json.dumps(new_image)}")
                    return process_temperature_data(new_image)
        elif 'temperature' in event:
            logger.info("Processando dados de temperatura do solo do evento")
            return process_temperature_data(event)
        else:
            logger.info("Coletando dados de temperatura do solo do IoT Core")
            iot_data = get_latest_temperature()
            if iot_data['statusCode'] == 200:
                temperature_data = json.loads(iot_data['body'])
                return process_temperature_data(temperature_data)
            else:
                logger.error(f"Falha ao obter dados do IoT Core: {iot_data['body']}")
                return iot_data

    except Exception as e:
        logger.error(f"Erro no lambda_handler: {str(e)}")
        return create_response(500, f"Erro interno: {str(e)}")

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
            return create_response(200, json.dumps(item))
        else:
            return create_response(404, "Plano de tarefas não encontrado")
    except Exception as e:
        logger.error(f"Erro ao obter plano de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter plano de tarefas: {str(e)}")

def get_all_task_plans():
    try:
        response = task_plan_table.scan()
        items = response.get('Items', [])
        return create_response(200, json.dumps(items))
    except Exception as e:
        logger.error(f"Erro ao obter todos os planos de tarefas: {str(e)}")
        return create_response(500, f"Erro ao obter todos os planos de tarefas: {str(e)}")

def process_temperature_data(data):
    try:
        logger.info(f"Dados recebidos para processamento: {data}")
        
        if isinstance(data, str):
            logger.info("Dados recebidos como string. Tentando converter para dicionário.")
            data = json.loads(data)
        
        if not isinstance(data, dict):
            logger.error(f"Formato de dados inesperado: {type(data)}")
            return {
                'statusCode': 400,
                'body': json.dumps('Formato de dados inválido')
            }
        
        temperature = data.get('temperature')
        status = data.get('status')
        
        if temperature is None:
            logger.error("Dados de temperatura ausentes")
            return {
                'statusCode': 400,
                'body': json.dumps('Dados de temperatura ausentes')
            }
        
        try:
            if not temperature:
                raise ValueError("Valor de temperatura vazio")
        except ValueError:
            logger.error(f"Valor de temperatura inválido: {temperature}")
            return {
                'statusCode': 400,
                'body': json.dumps('Valor de temperatura inválido')
            }
        
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
        
        return {
            'statusCode': 200,
            'body': json.dumps('Novo plano de tarefas gerado e armazenado')
        }
    except Exception as e:
        logger.error(f"Erro ao processar dados de temperatura: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Erro ao processar dados de temperatura: {str(e)}")
        }

def get_recommendations(topic):
    try:
        recommendation_prompt = f"""Forneça recomendações detalhadas para {topic} em uma fazenda, considerando a temperatura do solo e práticas agrícolas modernas e sustentáveis."""
        
        prompt = "Human: " + recommendation_prompt + "\n\nAssistant:"
        
        logger.info("Enviando prompt para o modelo de IA para o auxilio recomendação das tarefas...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
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

def generate_task_plan_with_ai(realtime_temperature, realtime_timestamp):
    try:
        # Obter recomendações para cada tópico
        soil_management_recommendations = get_recommendations("manejo do solo baseado na temperatura")
        planting_recommendations = get_recommendations("plantio considerando a temperatura do solo")
        crop_care_recommendations = get_recommendations("cuidados com as culturas baseados na temperatura do solo")
        irrigation_recommendations = get_recommendations("irrigação baseada na temperatura do solo")
        
        task_plan_prompt = f"""
        Com base nos seguintes dados de temperatura do solo e recomendações:
        Temperatura em Tempo Real: {realtime_temperature}°C

        Recomendações de Manejo do Solo:
        {soil_management_recommendations}

        Recomendações de Plantio:
        {planting_recommendations}

        Recomendações de Cuidados com as Culturas:
        {crop_care_recommendations}

        Recomendações de Irrigação:
        {irrigation_recommendations}

        Gere um plano detalhado de tarefas para as próximas 4 semanas, incluindo:
        1. Atividades de manejo do solo baseadas na temperatura
        2. Datas e horários recomendados para plantio
        3. Cuidados específicos com as culturas considerando a temperatura do solo
        4. Recomendações de irrigação ajustadas à temperatura do solo

        Forneça um plano estruturado com datas específicas e descrições das tarefas.
        Se não houver dados do último plano ou dados em tempo real, faça as melhores recomendações possíveis com base nas informações disponíveis e nas recomendações gerais.
        """
        
        prompt = "Human: " + task_plan_prompt + "\n\nAssistant:"

        logger.info("Enviando prompt para o modelo de IA para recomendação das tarefas...")
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 2000,
                "temperature": 0.5,
                "top_p": 0.9,
                "stop_sequences": ["\n\nHuman:"]
            })
        )
        
        response_body = json.loads(response['body'].read())
        task_plan_text = response_body['completion']
        
        logger.info("Plano de tarefas gerado com sucesso")
        logger.info(f"Texto do plano de tarefas: {task_plan_text}")
        return task_plan_text
    
    except Exception as e:
        logger.error(f"Erro ao gerar plano de tarefas com IA: {str(e)}")
        return None

def format_plan(raw_json):
    # Parse o JSON
    data = json.loads(raw_json)
    
    # Obtenha o plano e remova as sequências de escape
    plan = data['plan'].encode().decode('unicode_escape')
    
    # Corrija a formatação do campo 'plan'
    lines = plan.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line:
            if re.match(r'^[0-9]+\.', line):  # Se a linha começa com um número seguido de ponto
                formatted_lines.append(line)
            elif re.match(r'^-', line):  # Se a linha já começa com hífen
                formatted_lines.append(line)
            elif re.match(r'^[A-Z]', line):  # Se a linha começa com letra maiúscula
                formatted_lines.append(line)
            else:
                formatted_lines.append('- ' + line)
    
    # Atualize o campo 'plan' no JSON original
    data['plan'] = '\n'.join(formatted_lines)
    
    # Use json.dumps com indent=2 e ensure_ascii=False para manter a formatação
    return json.dumps(data, ensure_ascii=False, indent=2)

def parse_task_plan(task_plan_text):
    logger.info(f"Texto do plano de tarefas recebido:\n{task_plan_text}")

    # Primeiro, formate o JSON
    formatted_data = format_plan(task_plan_text)
    
    # Extraia o plano de tarefas do JSON formatado
    plan_text = formatted_data['plan']

    categories = {
        'manejo_solo': ['preparar', 'arar', 'gradear'],
        'plantio': ['plantar', 'semear'],
        'cuidados_culturas': ['monitorar', 'aplicar', 'podar', 'fertilizar'],
        'irrigação': ['irrigar', 'regar', 'ajustar']
    }
    parsed_task_plan = {key: {} for key in categories.keys()}
    parsed_task_plan['tarefas_avulsas'] = []
    
    lines = plan_text.split('\n')
    current_week = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.lower().startswith("semana") or line.lower() == "semanalmente:":
            current_week = line.rstrip(':')
            for category in categories.keys():
                if current_week not in parsed_task_plan[category]:
                    parsed_task_plan[category][current_week] = []
        elif line[0] == '-' or any(line.lower().startswith(day) for day in ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']):
            task = line.lstrip('- ')
            if current_week is None:
                parsed_task_plan['tarefas_avulsas'].append(task)
            else:
                category_found = False
                for category, keywords in categories.items():
                    if any(keyword in task.lower() for keyword in keywords):
                        parsed_task_plan[category][current_week].append(task)
                        category_found = True
                        break
                
                if not category_found:
                    parsed_task_plan['cuidados_culturas'][current_week].append(task)
        else:
            if current_week:
                parsed_task_plan['cuidados_culturas'][current_week].append(line)
            else:
                parsed_task_plan['tarefas_avulsas'].append(line)
    
    # Remove empty weeks and categories
    for category in list(parsed_task_plan.keys()):
        if category != 'tarefas_avulsas':
            parsed_task_plan[category] = {week: tasks for week, tasks in parsed_task_plan[category].items() if tasks}
            if not parsed_task_plan[category]:
                del parsed_task_plan[category]
    
    if not parsed_task_plan['tarefas_avulsas']:
        del parsed_task_plan['tarefas_avulsas']
    
    # Atualiza o plano no JSON formatado
    formatted_data['plan'] = parsed_task_plan

    logger.info(f"Plano de tarefas após parseamento e formatação: {json.dumps(formatted_data, indent=2)}")
    return formatted_data

def extract_plan_data(plan_text):
    # Decodificar caracteres escapados
    plan_text = plan_text.encode().decode('unicode_escape')

    # Extrair tarefas e culturas
    tasks = re.findall(r'- ([^-]+)', plan_text)
    crops = re.findall(r'(Plantio|Cuidados) (?:com|de) ([^\.]+)', plan_text)

    # Processar tarefas
    processed_tasks = []
    for task in tasks:
        task = task.strip()
        match = re.match(r'(\w+),?\s*(\d+h)?\s*-?\s*(.+)', task)
        if match:
            day, time, description = match.groups()
            processed_tasks.append({
                "day": day,
                "time": time if time else "N/A",
                "description": description.strip()
            })
        else:
            logger.warning(f"Formato de tarefa não reconhecido: {task}")
            processed_tasks.append({
                "day": "N/A",
                "time": "N/A",
                "description": task
            })

    # Processar culturas
    processed_crops = [crop[1] for crop in crops]

    logger.info(f"Tarefas processadas: {processed_tasks}")
    logger.info(f"Culturas processadas: {processed_crops}")

    return {
        'tasks': processed_tasks,
        'crops': list(set(processed_crops))  # Remove duplicatas
    }

def store_task_plan(task_plan, average_temperature, status):
    try:
        plan_id = str(uuid.uuid4())
        created_at = str(time.time() * 1000)  # Timestamp atual em milissegundos
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Extrair dados do plano
        extracted_data = extract_plan_data(task_plan)
        
        task_plan_item = {
            'planId': plan_id,
            'createdAt': created_at,
            'timestamp': timestamp,
            'averageTemperature': average_temperature,
            'status': status,
            'userId': 'default_user',
            'plan': json.dumps(task_plan),
            'extractedTasks': json.dumps(extracted_data['tasks']),
            'extractedCrops': json.dumps(extracted_data['crops'])
        }
        
        history_temperature_item = {
            'timestamp': timestamp,
            'averageTemperature': average_temperature,
            'planGenerated': 'Yes',
            'status': status
        }
        
        logger.info(f"Dados do task plan: {json.dumps(task_plan_item, default=str)}")
        logger.info(f"Dados do temperature history: {json.dumps(history_temperature_item, default=str)}")
        logger.info(f"Dados extraídos: {json.dumps(extracted_data, default=str)}")
        
        temperature_history_table.put_item(Item=history_temperature_item)
        temperature_history_table.put_item(Item=task_plan_item)
        task_plan_table.put_item(Item=task_plan_item)
        logger.info(f"Plano de tarefas armazenado com sucesso. ID: {plan_id}")
        
        return plan_id
    except Exception as e:
        logger.error(f"Erro ao armazenar plano de tarefas: {str(e)}")
        raise

def get_last_task_plan():
    try:
        response = task_plan_table.scan(
            Limit=1,
            ScanIndexForward=False
        )
        items = response.get('Items', [])
        if items:
            logger.info("Último plano de tarefas recuperado com sucesso")
            return items[0]
        else:
            logger.info("Nenhum plano de tarefas anterior encontrado")
            return {}
    except Exception as e:
        logger.error(f"Erro ao obter o último plano de tarefas: {str(e)}")
        return {}
    
def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': body
    }