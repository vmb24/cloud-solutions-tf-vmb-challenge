import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return marketplace_fulfillment(event, context)

def marketplace_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair o ID do usuário
        user_id = extract_user_id(intent_request, session_attributes)
        
        if not user_id:
            raise ValueError("ID do usuário não fornecido")

        # Preparar os dados para o handler específico
        handler_event = {
            'user_id': user_id
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['MARKETPLACE_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        relevant_products = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_product_recommendations(relevant_products)

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
        print(f"Erro no marketplace_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao buscar produtos relevantes para você.'
                }
            }
        }

def extract_user_id(intent_request, session_attributes):
    # Tenta extrair o user_id do intent_request ou session_attributes
    user_id = intent_request.get('userId')
    if not user_id:
        user_id = session_attributes.get('user_id')
    return user_id

def format_product_recommendations(products):
    if not products:
        return "Desculpe, não encontramos produtos relevantes para suas necessidades no momento."
    
    response = "Aqui estão alguns produtos que podem te interessar:\n\n"
    for product in products:
        response += f"Nome: {product['name']}\n"
        response += f"Preço: R$ {product['price']:.2f}\n"
        response += f"ID do Produto: {product['product_id']}\n\n"
    response += "Você gostaria de mais informações sobre algum desses produtos?"
    return response