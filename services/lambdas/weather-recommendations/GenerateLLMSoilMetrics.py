import os
import json
import boto3
from uuid import uuid4
from datetime import datetime, timezone
import subprocess

# AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LLMSoilMetrics'])

def get_jurassic2_response(prompt: str):
    # Usando AWS CLI para invocar o modelo Bedrock
    cmd = [
        'aws', 'bedrock-runtime', 'invoke-model',
        '--model-id', 'jurassic-2-mid',
        '--content-type', 'application/json',
        '--accept', 'application/json',
        '--body', json.dumps({"prompt": prompt, "maxTokens": 512}),
        '--region', os.environ['AWS_REGION']
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    response_body = json.loads(result.stdout)
    return response_body['outputs'][0]['output']

def generate_recommendations(query, context_data):
    prompt_template = """
    Você é um especialista em agricultura. Sua resposta final deverá ser um conjunto completo e detalhado de recomendações para otimizar a saúde e produção das plantas. 
    Utilize o contexto fornecido e o input do usuário para elaborar suas recomendações.
    Contexto: {context_data}
    Usuário: {query}
    Assistente:
    """
    
    full_prompt = prompt_template.format(context_data=context_data, query=query)
    response = get_jurassic2_response(full_prompt)
    return response
    
def save_recommendation(query, context_data, recommendation):
    recommendation_id = str(uuid4())
    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    table.put_item(
        Item={
            'recommendationId': recommendation_id,
            'query': query,
            'contextData': context_data,
            'recommendation': recommendation,
            'date': current_date
        }
    )
    return recommendation_id

def getResponse(query, context_data):
    recommendation = generate_recommendations(query, context_data)
    recommendation_id = save_recommendation(query, context_data, recommendation)
    return recommendation, recommendation_id

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'POST':
        body = json.loads(event.get('body', {}))
        query = body.get('question', 'Parametro question não fornecido')
        context_data = body.get('context_data', 'Parametro context_data não fornecido')
        recommendation, recommendation_id = getResponse(query, context_data)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Tarefa concluída com sucesso",
                "recommendation_id": recommendation_id,
                "details": recommendation
            }),
        }
    
    elif http_method == 'GET':
        recommendations = table.scan()['Items']
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Recomendações recuperadas com sucesso",
                "recommendations": recommendations
            }),
        }
    
    else:
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Método não permitido"
            }),
        }
