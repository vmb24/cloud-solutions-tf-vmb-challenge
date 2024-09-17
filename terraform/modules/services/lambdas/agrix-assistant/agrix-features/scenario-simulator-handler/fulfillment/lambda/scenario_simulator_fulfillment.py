import json
import boto3
import os

# Inicializar o cliente Lambda
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de fulfillment.
    """
    return scenario_simulator_fulfillment(event, context)

def scenario_simulator_fulfillment(event, context):
    try:
        # Extrair informações relevantes do evento
        intent_request = event.get('intentRequest', {})
        session_attributes = event.get('sessionAttributes', {})
        
        # Extrair os parâmetros do cenário do intent_request
        scenario_params = extract_scenario_params(intent_request)
        
        if not scenario_params:
            raise ValueError("Parâmetros do cenário não fornecidos")

        # Preparar os dados para o handler específico
        handler_event = {
            'scenario_params': scenario_params
        }

        # Invocar o handler específico
        response = lambda_client.invoke(
            FunctionName=os.environ['SCENARIO_SIMULATOR_HANDLER_ARN'],
            InvocationType='RequestResponse',
            Payload=json.dumps(handler_event)
        )

        # Processar a resposta do handler
        handler_response = json.loads(response['Payload'].read().decode())
        simulation_results = json.loads(handler_response['body'])

        # Preparar a resposta para o usuário
        user_response = format_simulation_results(simulation_results)

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
        print(f"Erro no scenario_simulator_fulfillment: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao simular o cenário.'
                }
            }
        }

def extract_scenario_params(intent_request):
    # Extrair os parâmetros do cenário do intent_request
    # Isso dependerá de como os slots estão configurados no seu bot
    slots = intent_request.get('currentIntent', {}).get('slots', {})
    return {
        'crop_type': slots.get('CropType'),
        'area_size': float(slots.get('AreaSize', 0)),
        'irrigation_type': slots.get('IrrigationType'),
        'fertilizer_type': slots.get('FertilizerType'),
        'pest_control_method': slots.get('PestControlMethod')
    }

def format_simulation_results(results):
    yield_projection = results['yield_projection']
    profit_projection = results['profit_projection']
    risk_assessment = results['risk_assessment']
    
    response = f"Baseado nos parâmetros fornecidos, nossa simulação de cenário projeta o seguinte:\n\n"
    response += f"Produção estimada: {yield_projection} kg/hectare\n"
    response += f"Projeção de lucro: ${profit_projection:,.2f}\n"
    response += f"Avaliação de risco: {risk_assessment}\n\n"
    response += "Lembre-se que esta é uma simulação baseada em modelos e dados históricos. "
    response += "As condições reais podem variar e é sempre recomendável consultar um agrônomo para decisões importantes."
    
    return response