import datetime
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Adicionar headers CORS para todas as respostas
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,PUT'
    }

    # Tratar requisições OPTIONS para CORS
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS preflight request successful')
        }

    try:
        # Extrair o userId do corpo da requisição
        body = json.loads(event['body'])
        user_id = body['userId']
        
        # Tentar obter o usuário do DynamoDB
        try:
            response = table.get_item(Key={'UserId': user_id})
            if 'Item' in response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps('Usuário já existe')
                }
        except ClientError as e:
            print(e.response['Error']['Message'])
        
        # Se o usuário não existir, criar um novo
        table.put_item(
            Item={
                'UserId': user_id,
                'CreatedAt': str(datetime.datetime.now())
            },
            ConditionExpression='attribute_not_exists(UserId)'
        )
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps('Novo usuário criado')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps('Erro ao processar a requisição')
        }