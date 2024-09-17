import json
import boto3
import base64
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return image_diagnosis_fulfillment(event, context)

def image_diagnosis_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair a imagem do intent_request
        image_url = intent_request.get('inputTranscript')
        
        if not image_url:
            raise ValueError("URL da imagem não fornecida")

        # Baixar a imagem da URL
        image_bytes = download_image(image_url)

        # Preparar os dados para o handler específico
        handler_event = {
            'image': base64.b64encode(image_bytes).decode('utf-8')
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['IMAGE_DIAGNOSIS_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        diagnosis = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_diagnosis_response(diagnosis)

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
        print(f"Erro no image_diagnosis_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao analisar a imagem.'
                }
            }
        }

def download_image(url):
    import requests
    response = requests.get(url)
    return response.content

def format_diagnosis_response(diagnosis):
    response = f"Diagnóstico: {diagnosis['diagnosis']}\n"
    response += f"Confiança: {diagnosis['confidence']*100:.2f}%\n\n"
    
    if 'recommendations' in diagnosis:
        response += "Recomendações:\n"
        for rec in diagnosis['recommendations']:
            response += f"- {rec}\n"
    
    return response