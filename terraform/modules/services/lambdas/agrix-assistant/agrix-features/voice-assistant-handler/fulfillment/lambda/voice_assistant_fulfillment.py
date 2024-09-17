import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return voice_assistant_fulfillment(event, context)

def voice_assistant_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair a mensagem do intent_request
        message = extract_message(intent_request)
        
        if not message:
            raise ValueError("Mensagem não fornecida")

        # Preparar os dados para o handler específico
        handler_event = {
            'message': message
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['VOICE_ASSISTANT_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        audio_url = json.loads(handler_response['body'])['audio_url']

        # Preparar a resposta para o usuário
        user_response = format_voice_response(audio_url)

        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'CustomPayload',
                    'content': json.dumps(user_response)
                }
            }
        }
    except Exception as e:
        print(f"Erro no voice_assistant_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao processar sua solicitação de voz.'
                }
            }
        }

def extract_message(intent_request):
    # Extrair a mensagem do intent_request
    # Isso dependerá de como os slots estão configurados no seu bot
    slots = intent_request.get('currentIntent', {}).get('slots', {})
    return slots.get('Message')

def format_voice_response(audio_url):
    return {
        'audioUrl': audio_url,
        'text': "Aqui está o áudio que você solicitou. Clique para ouvir."
    }