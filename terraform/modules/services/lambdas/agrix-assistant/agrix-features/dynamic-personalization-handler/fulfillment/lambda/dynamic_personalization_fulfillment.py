import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return dynamic_personalization_fulfillment(event, context)

def dynamic_personalization_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair o ID do usuário do intent_request ou session_attributes
        user_id = intent_request.get('userId') or session_attributes.get('userId')
        
        if not user_id:
            raise ValueError("ID do usuário não fornecido")

        # Preparar os dados para o handler específico
        handler_event = {
            'user_id': user_id,
            'session_attributes': session_attributes
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['DYNAMIC_PERSONALIZATION_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        personalized_content = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_user_response(personalized_content)

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
        print(f"Erro no dynamic_personalization_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao personalizar o conteúdo.'
                }
            }
        }

def format_user_response(personalized_content):
    response = "Aqui está seu conteúdo personalizado:\n\n"
    
    if 'content' in personalized_content:
        response += personalized_content['content'] + "\n"
    
    if 'recommendations' in personalized_content:
        response += "\nRecomendações personalizadas:\n"
        for rec in personalized_content['recommendations']:
            response += f"- {rec}\n"
    
    if 'custom_message' in personalized_content:
        response += f"\n{personalized_content['custom_message']}\n"
    
    return response