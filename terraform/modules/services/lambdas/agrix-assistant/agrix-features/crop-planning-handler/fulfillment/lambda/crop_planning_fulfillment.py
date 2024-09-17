import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return crop_planning_fulfillment(event, context)

def crop_planning_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair dados da fazenda do intent_request
        farm_data = intent_request.get('farmData', {})

        # Preparar os dados para o handler específico
        handler_event = {
            'farm_data': farm_data,
            'session_attributes': session_attributes
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['CROP_PLANNING_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        optimized_plan = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_user_response(optimized_plan)

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
        print(f"Erro no crop_planning_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao gerar o plano de cultivo.'
                }
            }
        }

def format_user_response(optimized_plan):
    response = "Aqui está seu plano de cultivo otimizado:\n\n"
    response += "Rotação de Culturas:\n"
    for i, crop in enumerate(optimized_plan['crop_rotation']):
        date = optimized_plan['planting_dates'][i]
        response += f"- {crop}: Plantio em {date}\n"
    
    if 'expected_yield' in optimized_plan:
        response += f"\nProdutividade esperada: {optimized_plan['expected_yield']} ton/ha\n"
    
    if 'recommendations' in optimized_plan:
        response += "\nRecomendações adicionais:\n"
        for rec in optimized_plan['recommendations']:
            response += f"- {rec}\n"
    
    return response