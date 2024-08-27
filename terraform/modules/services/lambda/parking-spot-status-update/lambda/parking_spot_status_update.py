import json
import time
import logging
from botocore.exceptions import ClientError
import boto3
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingSpots')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        logger.info("Iniciando atualização de vaga de estacionamento")
        logger.info(f"Evento completo recebido: {json.dumps(event)}")
        
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        logger.info(f"Body extraído: {json.dumps(body)}")
        
        if 'pathParameters' in event and event['pathParameters'] and 'id' in event['pathParameters']:
            spot_id = event['pathParameters']['id']
        elif 'spot_id' in body:
            spot_id = body['spot_id']
        else:
            raise ValueError("spot_id não encontrado no evento")
        
        logger.info(f"Atualizando vaga com ID: {spot_id}")
        
        update_expression_parts = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        updatable_fields = ['name', 'latitude', 'longitude', 'status', 'description']

        for key, value in body.items():
            if key in updatable_fields:
                update_expression_parts.append(f"#{key} = :{key}")
                expression_attribute_names[f"#{key}"] = key
                expression_attribute_values[f":{key}"] = value
                logger.info(f"Atualizando campo {key} com valor {value}")

        # Determinar a disponibilidade com base no status
        if 'status' in body:
            status = body['status'].lower()
            if status == 'disponível':
                availability = True
            elif status == 'ocupada':
                availability = False
            else:
                logger.warning(f"Status não reconhecido: {status}. Availability não será atualizado.")
            
            if 'availability' in locals():
                update_expression_parts.append("#availability = :availability")
                expression_attribute_names["#availability"] = "availability"
                expression_attribute_values[":availability"] = availability
                logger.info(f"Definindo availability como {availability} baseado no status {body['status']}")

        if not update_expression_parts:
            logger.warning("Nenhum campo válido para atualização")
            return {
                'statusCode': 400,
                'body': json.dumps('Nenhum campo válido para atualização')
            }

        update_expression = "SET " + ", ".join(update_expression_parts)
        update_expression += ", last_updated = :last_updated"
        expression_attribute_values[':last_updated'] = int(time.time())

        logger.info(f"Expressão de atualização: {update_expression}")
        logger.info(f"Valores dos atributos: {json.dumps(expression_attribute_values, default=decimal_default)}")
        logger.info(f"Nomes dos atributos: {json.dumps(expression_attribute_names)}")

        response = table.update_item(
            Key={'spot_id': spot_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW"
        )

        logger.info("Vaga atualizada com sucesso")
        logger.info(f"Resposta do DynamoDB: {json.dumps(response, default=decimal_default)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Vaga atualizada com sucesso',
                'updatedItem': response['Attributes']
            }, default=decimal_default)
        }
    except ClientError as e:
        logger.error(f"Erro ao atualizar a vaga: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao atualizar a vaga: {str(e)}')
        }
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar a vaga: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro inesperado ao atualizar a vaga: {str(e)}')
        }