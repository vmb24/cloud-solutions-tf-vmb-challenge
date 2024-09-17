import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return learning_module_fulfillment(event, context)

def learning_module_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair o user_id do session_attributes
        user_id = session_attributes.get('user_id')
        
        if not user_id:
            raise ValueError("ID do usuário não fornecido")

        # Preparar os dados para o handler específico
        handler_event = {
            'user_id': user_id
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['LEARNING_MODULE_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        next_module = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_module_response(next_module)

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
        print(f"Erro no learning_module_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao buscar o próximo módulo de aprendizagem.'
                }
            }
        }

def format_module_response(module):
    response = f"Seu próximo módulo de aprendizagem está pronto:\n\n"
    response += f"Título: {module['title']}\n"
    response += f"ID do Módulo: {module['module_id']}\n\n"
    response += f"Conteúdo: {module['content'][:100]}...\n\n"  # Mostra apenas os primeiros 100 caracteres do conteúdo
    response += "Você pode acessar o conteúdo completo no nosso portal de aprendizagem."
    return response