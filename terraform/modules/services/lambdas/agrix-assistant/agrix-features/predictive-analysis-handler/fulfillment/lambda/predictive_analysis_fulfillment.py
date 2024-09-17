import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return predictive_analysis_fulfillment(event, context)

def predictive_analysis_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair os dados atuais do intent_request
        current_data = extract_current_data(intent_request)
        
        if not current_data:
            raise ValueError("Dados atuais não fornecidos")

        # Preparar os dados para o handler específico
        handler_event = {
            'current_data': current_data
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['PREDICTIVE_ANALYSIS_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        analysis_result = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_analysis_result(analysis_result)

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
        print(f"Erro no predictive_analysis_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao realizar a análise preditiva.'
                }
            }
        }

def extract_current_data(intent_request):
    # Extrair os dados atuais do intent_request
    # Isso dependerá de como os slots estão configurados no seu bot
    slots = intent_request.get('currentIntent', {}).get('slots', {})
    return {
        'temperature': float(slots.get('Temperature', 0)),
        'humidity': float(slots.get('Humidity', 0)),
        'soil_moisture': float(slots.get('SoilMoisture', 0)),
        'rainfall': float(slots.get('Rainfall', 0))
    }

def format_analysis_result(result):
    prediction = result['prediction']
    recommendations = result['recommendations']
    
    response = f"Baseado nos dados fornecidos, nossa análise preditiva indica um risco de: {prediction}\n\n"
    response += f"Recomendações: {recommendations}\n\n"
    response += "Lembre-se de que esta é uma previsão baseada em dados históricos e nas condições atuais. "
    response += "Sempre monitore sua plantação de perto e consulte um agrônomo se necessário."
    
    return response