import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return compliance_assistant_fulfillment(event, context)

def compliance_assistant_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair práticas agrícolas do intent_request
        farm_practices = intent_request.get('farmPractices', {})

        # Preparar os dados para o handler específico
        handler_event = {
            'farm_practices': farm_practices,
            'session_attributes': session_attributes
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['COMPLIANCE_ASSISTANT_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        compliance_check = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_user_response(compliance_check)

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
        print(f"Erro no compliance_assistant_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao verificar a conformidade.'
                }
            }
        }

def format_user_response(compliance_check):
    if compliance_check['compliant']:
        response = "Suas práticas agrícolas estão em conformidade com as regulamentações atuais. "
    else:
        response = "Foram identificadas algumas áreas que precisam de atenção para garantir total conformidade. "

    if compliance_check['recommendations']:
        response += "Recomendações:\n"
        for rec in compliance_check['recommendations']:
            response += f"- {rec}\n"
    
    return response