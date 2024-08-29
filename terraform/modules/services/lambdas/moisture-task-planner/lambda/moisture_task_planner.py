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

task_plan_table = dynamodb.Table('TaskPlans')
moisture_history_table = dynamodb.Table('MoistureHistory')

IOT_THING_NAME = "moisture_sensor"

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        if 'Records' in event:
            for record in event['Records']:
                if record['eventName'] == 'INSERT':
                    new_image = record['dynamodb']['NewImage']
                    logger.info(f"Novo registro inserido na tabela MoistureHistory: {json.dumps(new_image)}")
                    return process_moisture_data(new_image)
        elif 'moisture' in event:
            logger.info("Processando dados de umidade do evento")
            return process_moisture_data(event)
        else:
            logger.info("Coletando dados de umidade do IoT Core")
            iot_data = get_latest_moisture()
            if iot_data['statusCode'] == 200:
                moisture_data = json.loads(iot_data['body'])
                return process_moisture_data(moisture_data)
            else:
                logger.error(f"Falha ao obter dados do IoT Core: {iot_data['body']}")
                return iot_data

    except Exception as e:
        logger.error(f"Erro no lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Erro interno: {str(e)}")
        }

def get_latest_moisture():
    try:
        logger.info(f"Tentando obter shadow para o dispositivo: {IOT_THING_NAME}")
        response = iot_client.get_thing_shadow(thingName=IOT_THING_NAME)
        payload = json.loads(response['payload'].read().decode())
        logger.info(f"Payload do shadow recebido: {payload}")
        state = payload['state']['reported']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'moisture': state['moisture'],
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

def process_moisture_data(data):
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
        
        moisture = data.get('moisture')
        status = data.get('status')
        
        if moisture is None:
            logger.error("Dados de umidade ausentes")
            return {
                'statusCode': 400,
                'body': json.dumps('Dados de umidade ausentes')
            }
        
        try:
            if not moisture:
                raise ValueError("Valor de umidade vazio")
        except ValueError:
            logger.error(f"Valor de umidade inválido: {moisture}")
            return {
                'statusCode': 400,
                'body': json.dumps('Valor de umidade inválido')
            }
        
        logger.info(f"Processando dados de umidade: moisture={moisture}, status={status}")
        
        new_plan = generate_task_plan_with_ai(moisture, status)
        if new_plan:
            plan_id = store_task_plan(new_plan, moisture, status)
            if plan_id:
                logger.error("Sucesso ao armazenar o plano de tarefas")
                # invoke_image_generation_lambda(plan_id, new_plan)
                # invoke_video_generation_lambda(plan_id, new_plan)
            else:
                logger.error("Falha ao armazenar o plano de tarefas")
        else:
            logger.error("Falha ao gerar o plano de tarefas")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Novo plano de tarefas gerado e armazenado')
        }
    except Exception as e:
        logger.error(f"Erro ao processar dados de umidade: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Erro ao processar dados de umidade: {str(e)}")
        }

def get_recommendations(topic):
    try:
        recommendation_prompt = f"""Human: Forneça recomendações detalhadas para {topic} em uma fazenda, considerando práticas agrícolas modernas e sustentáveis. Assistant:"""
        
        prompt = "Human: " + recommendation_prompt + "\n\nAssistant:"
        
        logger.info("Enviando prompt para o modelo de IA para o auxilio recomemdação das tarefas...")
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
        return recommendations.strip()
    except Exception as e:
        logger.error(f"Erro ao obter recomendações para {topic}: {str(e)}")
        return f"Não foi possível obter recomendações para {topic} devido a um erro."

def generate_task_plan_with_ai(realtime_moisture, realtime_timestamp):
    try:
        # last_plan = get_last_task_plan()
        # last_moisture = last_plan.get('AverageMoisture', 'N/A')
        # last_timestamp = last_plan.get('Timestamp', 'N/A')
        
        # Obter recomendações para cada tópico
        harvest_recommendations = get_recommendations("colheita")
        planting_recommendations = get_recommendations("plantio")
        maintenance_recommendations = get_recommendations("manutenção")
        irrigation_recommendations = get_recommendations("irrigação")
        
        task_plan_prompt = f"""
        Com base nos seguintes dados de umidade do solo e recomendações:
        Umidade em Tempo Real: {realtime_moisture}

        Recomendações de Colheita:
        {harvest_recommendations}

        Recomendações de Plantio:
        {planting_recommendations}

        Recomendações de Manutenção:
        {maintenance_recommendations}

        Recomendações de Irrigação:
        {irrigation_recommendations}

        Gere um plano detalhado de tarefas para as próximas 4 semanas, incluindo:
        1. Datas e horários recomendados para colheita
        2. Datas e horários recomendados para plantio
        3. Atividades de manutenção necessárias
        4. Recomendações de irrigação

        Forneça um plano estruturado com datas específicas e descrições das tarefas.
        Se não houver dados do último plano ou dados em tempo real, faça as melhores recomendações possíveis com base nas informações disponíveis e nas recomendações gerais.
        """
        
        prompt = "Human: " + task_plan_prompt + "\n\nAssistant:"

        logger.info("Enviando prompt para o modelo de IA para recomemdação das tarefas...")
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
        'colheita': ['colher'],
        'plantio': ['plantar'],
        'manutenção': ['capinar', 'remover', 'verificar', 'aplicar', 'monitorar', 'adubar', 'podar'],
        'irrigação': ['irrigar', 'umidade', 'água']
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
                    parsed_task_plan['manutenção'][current_week].append(task)
        else:
            if current_week:
                parsed_task_plan['manutenção'][current_week].append(line)
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
    crops = re.findall(r'(Colheita|Plantio|Poda) d[ea] ([^\.]+)', plan_text)

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

def store_task_plan(task_plan, average_moisture, status):
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
            'averageMoisture': average_moisture,
            'status': status,
            'userId': 'default_user',
            'plan': json.dumps(task_plan),
            'extractedTasks': json.dumps(extracted_data['tasks']),
            'extractedCrops': json.dumps(extracted_data['crops'])
        }
        
        history_moisture_item = {
            'timestamp': timestamp,
            'averageMoisture': average_moisture,
            'planGenerated': 'Yes',
            'status': status
        }
        
        logger.info(f"Dados do task plan: {json.dumps(task_plan_item, default=str)}")
        logger.info(f"Dados do moisture history: {json.dumps(history_moisture_item, default=str)}")
        logger.info(f"Dados extraídos: {json.dumps(extracted_data, default=str)}")
        
        moisture_history_table.put_item(Item=history_moisture_item)
        moisture_history_table.put_item(Item=task_plan_item)
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

# def invoke_image_generation_lambda(plan_id, task_plan):
#     try:
#         payload = {
#             'plan_id': plan_id,
#             'task_plan': task_plan
#         }
#         response = lambda_client.invoke(
#             FunctionName='ImageGenerationLambda',
#             InvocationType='Event',
#             Payload=json.dumps(payload)
#         )
#         logger.info(f"Lambda de geração de imagem invocada com sucesso. StatusCode: {response['StatusCode']}")
#     except Exception as e:
#         logger.error(f"Erro ao invocar Lambda de geração de imagem: {str(e)}")

# def invoke_video_generation_lambda(plan_id, task_plan):
#     try:
#         payload = {
#             'plan_id': plan_id,
#             'task_plan': task_plan
#         }
#         response = lambda_client.invoke(
#             FunctionName='VideoGenerationLambda',
#             InvocationType='Event',
#             Payload=json.dumps(payload)
#         )
#         logger.info(f"Lambda de geração de vídeo invocada com sucesso. StatusCode: {response['StatusCode']}")
#     except Exception as e:
#         logger.error(f"Erro ao invocar Lambda de geração de vídeo: {str(e)}")