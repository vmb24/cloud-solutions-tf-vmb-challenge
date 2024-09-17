import boto3
import json
import os
import base64

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return ar_processor_fulfillment(event, context)

def ar_processor_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair a imagem do intent_request (assumindo que está em base64)
        image_base64 = intent_request.get('imageData', '')

        # Preparar os dados para o handler específico
        handler_event = {
            'image': image_base64,
            'session_attributes': session_attributes
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['AR_PROCESSOR_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        overlays = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_user_response(overlays)

        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': user_response
                }
            }
        }
    except Exception as e:
        print(f"Erro no ar_processor_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao processar sua imagem.'
                }
            }
        }

def format_user_response(overlays):
    response = "Elementos identificados na imagem:\n"
    for overlay in overlays:
        response += f"- {overlay['label']} (confiança: {overlay['confidence']:.2f}%)\n"
    return response