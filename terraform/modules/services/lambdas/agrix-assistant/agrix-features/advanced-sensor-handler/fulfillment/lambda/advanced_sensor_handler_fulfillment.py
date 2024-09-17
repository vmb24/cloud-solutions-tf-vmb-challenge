import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda.
    Esta é a função que a AWS Lambda chama quando a função é invocada.
    """
    return advanced_sensor_handler_fulfillment(event, context)

def advanced_sensor_handler_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Preparar os dados para o handler específico
        handler_event = {
            'sensor_data': intent_request.get('sensorData', {}),
            'session_attributes': session_attributes
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['ADVANCED_SENSOR_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        interpreted_data = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_user_response(interpreted_data)

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
        print(f"Erro no advanced_sensor_handler_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao processar sua solicitação.'
                }
            }
        }

def format_user_response(interpreted_data):
    soil_composition = interpreted_data.get('soil_composition', {})
    return (f"Baseado nos dados dos sensores avançados, a composição do solo é:\n"
            f"Nitrogênio: {soil_composition.get('nitrogen', 0):.2f}\n"
            f"Fósforo: {soil_composition.get('phosphorus', 0):.2f}\n"
            f"Potássio: {soil_composition.get('potassium', 0):.2f}")