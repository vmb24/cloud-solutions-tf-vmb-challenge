import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return knowledge_sharing_fulfillment(event, context)

def knowledge_sharing_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair a consulta do intent_request
        query = intent_request.get('inputTranscript')
        
        if not query:
            raise ValueError("Consulta não fornecida")

        # Preparar os dados para o handler específico
        handler_event = {
            'query': query
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['KNOWLEDGE_SHARING_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        solutions = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_solutions_response(solutions)

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
        print(f"Erro no knowledge_sharing_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao buscar as soluções.'
                }
            }
        }

def format_solutions_response(solutions):
    if not solutions:
        return "Desculpe, não encontrei nenhuma solução relevante para sua consulta."
    
    response = "Encontrei as seguintes soluções relevantes:\n\n"
    for i, sol in enumerate(solutions, 1):
        response += f"{i}. Problema: {sol['problem']}\n"
        response += f"   Solução: {sol['solution']}\n\n"
    
    return response