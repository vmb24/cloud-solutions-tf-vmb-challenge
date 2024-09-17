import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return marketing_assistant_fulfillment(event, context)

def marketing_assistant_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair os dados do produto do intent_request
        product_data = extract_product_data(intent_request)
        
        if not product_data:
            raise ValueError("Dados do produto não fornecidos")

        # Preparar os dados para o handler específico
        handler_event = {
            'product_data': product_data
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['MARKETING_ASSISTANT_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        market_analysis = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_market_analysis(market_analysis)

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
        print(f"Erro no marketing_assistant_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao analisar o mercado para o seu produto.'
                }
            }
        }

def extract_product_data(intent_request):
    # Extrair os dados do produto do intent_request
    # Isso dependerá de como os slots estão configurados no seu bot
    slots = intent_request.get('currentIntent', {}).get('slots', {})
    return {
        'product_name': slots.get('ProductName'),
        'product_type': slots.get('ProductType'),
        'price_range': slots.get('PriceRange'),
        'target_audience': slots.get('TargetAudience')
    }

def format_market_analysis(analysis):
    response = "Aqui está a análise de mercado para o seu produto:\n\n"
    response += f"Preço previsto: R$ {analysis['predicted_price']:.2f}\n"
    response += f"Previsão de demanda: {analysis['demand_forecast']}\n"
    response += f"Melhores mercados: {', '.join(analysis['best_markets'])}\n\n"
    response += "Com base nesta análise, recomendamos ajustar sua estratégia de marketing conforme necessário."
    return response