import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AgricultureTasks')  # Substitua pelo nome real da sua tabela

def lambda_handler(event, context):
    # Configuração CORS
    headers = {
        'Access-Control-Allow-Origin': '*',  # Ajuste para o domínio específico em produção
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }

    # Tratamento para requisição OPTIONS (preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS preflight successful')
        }

    # Roteamento baseado no método HTTP
    if event['httpMethod'] == 'GET':
        return get_tasks(event, headers)
    elif event['httpMethod'] == 'POST':
        return update_task_with_sensor_data(event, headers)
    else:
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps('Method Not Allowed')
        }

def get_tasks(event, headers):
    query_params = event.get('queryStringParameters', {})
    start_date = query_params.get('start_date')
    end_date = query_params.get('end_date')
    task_type = query_params.get('task_type')

    try:
        if start_date and end_date:
            response = table.query(
                KeyConditionExpression=Key('date').between(start_date, end_date)
            )
        else:
            response = table.scan()

        tasks = response['Items']

        if task_type:
            tasks = [task for task in tasks if task['task_type'] == task_type]

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(tasks)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Error getting tasks: {str(e)}')
        }

def update_task_with_sensor_data(event, headers):
    try:
        sensor_data = json.loads(event['body'])
        task_type = sensor_data.get('task_type')
        value = sensor_data.get('value')
        timestamp = sensor_data.get('timestamp', datetime.now().isoformat())

        if not task_type or value is None:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('task_type and value are required')
            }

        # Buscar a tarefa mais recente do tipo especificado
        response = table.query(
            KeyConditionExpression=Key('task_type').eq(task_type),
            ScanIndexForward=False,  # ordem decrescente
            Limit=1
        )

        if not response['Items']:
            # Se não existir, cria uma nova tarefa
            new_task = {
                'task_type': task_type,
                'date': timestamp,
                'value': value,
                'last_updated': timestamp
            }
            table.put_item(Item=new_task)
            message = 'New task created'
        else:
            # Se existir, atualiza a tarefa existente
            existing_task = response['Items'][0]
            table.update_item(
                Key={
                    'task_type': task_type,
                    'date': existing_task['date']
                },
                UpdateExpression='SET #val = :val, last_updated = :updated',
                ExpressionAttributeNames={
                    '#val': 'value'
                },
                ExpressionAttributeValues={
                    ':val': value,
                    ':updated': timestamp
                }
            )
            message = 'Task updated'

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': message,
                'task_type': task_type,
                'value': value,
                'timestamp': timestamp
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Error updating task: {str(e)}')
        }