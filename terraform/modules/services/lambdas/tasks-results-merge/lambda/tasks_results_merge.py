import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Configuração CORS
    headers = {
        'Access-Control-Allow-Origin': '*',  # Ajuste para o domínio específico em produção
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
    }

    # Tratamento para requisição OPTIONS (preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS preflight successful')
        }

    if event['httpMethod'] != 'GET':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps('Method Not Allowed')
        }

    # Parâmetros da query
    query_params = event.get('queryStringParameters', {})
    start_date = query_params.get('start_date')
    end_date = query_params.get('end_date')

    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('AgricultureTasks')  # Substitua pelo nome real da sua tabela

    try:
        if start_date and end_date:
            # Buscar tarefas por intervalo de data
            response = table.query(
                KeyConditionExpression=Key('date').between(start_date, end_date)
            )
        else:
            # Buscar todas as tarefas
            response = table.scan()

        tasks = response['Items']

        # Processar e mesclar os resultados
        merged_results = {
            'air_moisture': [],
            'air_temperature': [],
            'brightness': [],
            'soil_moisture': [],
            'soil_temperature': []
        }

        for task in tasks:
            task_type = task['task_type']
            if task_type in merged_results:
                merged_results[task_type].append(task)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Resultados mesclados com sucesso',
                'merged_results': merged_results
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Erro ao processar a requisição: {str(e)}')
        }