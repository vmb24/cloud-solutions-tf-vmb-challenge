import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return sustainability_assistant_fulfillment(event, context)

def sustainability_assistant_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair as práticas agrícolas do intent_request
        farm_practices = extract_farm_practices(intent_request)
        
        if not farm_practices:
            raise ValueError("Práticas agrícolas não fornecidas")

        # Preparar os dados para o handler específico
        handler_event = {
            'farm_practices': farm_practices
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['SUSTAINABILITY_ASSISTANT_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        sustainability_analysis = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_sustainability_analysis(sustainability_analysis)

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
        print(f"Erro no sustainability_assistant_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao analisar as práticas de sustentabilidade.'
                }
            }
        }

def extract_farm_practices(intent_request):
    # Extrair as práticas agrícolas do intent_request
    # Isso dependerá de como os slots estão configurados no seu bot
    slots = intent_request.get('currentIntent', {}).get('slots', {})
    return {
        'irrigation_method': slots.get('IrrigationMethod'),
        'fertilizer_use': slots.get('FertilizerUse'),
        'pest_control': slots.get('PestControl'),
        'soil_management': slots.get('SoilManagement'),
        'crop_rotation': slots.get('CropRotation', 'No')
    }

def format_sustainability_analysis(analysis):
    score = analysis['score']
    recommendations = analysis['recommendations']
    
    response = f"Com base nas práticas agrícolas fornecidas, sua pontuação de sustentabilidade é {score}/100.\n\n"
    response += "Recomendações para melhorar a sustentabilidade:\n"
    for i, recommendation in enumerate(recommendations, 1):
        response += f"{i}. {recommendation}\n"
    
    response += "\nLembre-se que essas recomendações são baseadas em análises gerais. "
    response += "Para um plano de sustentabilidade mais detalhado, considere consultar um especialista em agricultura sustentável."
    
    return response