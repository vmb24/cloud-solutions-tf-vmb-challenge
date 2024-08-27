import json
import boto3
import time
from decimal import Decimal
import logging
import uuid

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingSpots')

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    http_method = event['httpMethod']
    
    if http_method == 'POST':
        return create_parking_spot(event)
    elif http_method == 'DELETE':
        return remove_parking_spot(event)
    elif http_method == 'GET':
        return get_parking_spot(event)
    else:
        logger.warning(f"Método HTTP não suportado: {http_method}")
        return {
            'statusCode': 400,
            'body': json.dumps('Método não suportado')
        }

def create_parking_spot(event):
    try:
        logger.info("Iniciando criação de vaga de estacionamento")
        body = json.loads(event['body'])
        logger.info(f"Corpo da requisição: {json.dumps(body)}")
        
        # Validar campos obrigatórios
        required_fields = ['name', 'latitude', 'longitude', 'availability']
        for field in required_fields:
            if field not in body:
                logger.warning(f"Campo obrigatório ausente: {field}")
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'Campo obrigatório ausente: {field}')
                }
        
        # Validar latitude e longitude
        try:
            lat = float(body['latitude'])
            lon = float(body['longitude'])
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                logger.warning(f"Latitude ou longitude inválida: {lat}, {lon}")
                return {
                    'statusCode': 400,
                    'body': json.dumps('Latitude ou longitude inválida')
                }
        except ValueError:
            logger.warning(f"Erro ao converter latitude ou longitude para float")
            return {
                'statusCode': 400,
                'body': json.dumps('Latitude ou longitude inválida (não é um número)')
            }
        
        # Validar disponibilidade
        if body['availability'] not in ['disponível', 'ocupado']:
            logger.warning(f"Disponibilidade inválida: {body['availability']}")
            return {
                'statusCode': 400,
                'body': json.dumps('Disponibilidade deve ser "disponível" ou "ocupado"')
            }
        
        # Gerar um novo UUID para spot_id
        spot_id = str(uuid.uuid4())
        
        item = {
            'spot_id': spot_id,
            'name': body['name'],
            'latitude': Decimal(str(body['latitude'])),
            'longitude': Decimal(str(body['longitude'])),
            'availability': body['availability'],
            'status': body['availability'],
            'distance': Decimal('0'),
            'last_updated': int(time.time()),
            'description': body.get('description', '')
        }
        
        logger.info(f"Tentando inserir item no DynamoDB: {json.dumps(item, default=str)}")
        table.put_item(Item=item)
        
        logger.info("Vaga criada com sucesso")
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Vaga criada com sucesso',
                'spot_id': spot_id
            })
        }
    except Exception as e:
        logger.error(f"Erro ao criar a vaga: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao criar a vaga: {str(e)}')
        }
        
def remove_parking_spot(event):
    parking_spot_id = event['pathParameters']['id']
    
    table.delete_item(Key={'parking_spot_id': parking_spot_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps('Vaga removida com sucesso')
    }

def get_parking_spot(event):
    parking_spot_id = event['pathParameters'].get('id')
    
    if parking_spot_id:
        # Buscar uma vaga específica
        response = table.get_item(Key={'parking_spot_id': parking_spot_id})
        item = response.get('Item')
        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Vaga não encontrada')
            }
    else:
        # Listar todas as vagas
        response = table.scan()
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }