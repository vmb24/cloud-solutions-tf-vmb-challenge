import json
import boto3
import os
import logging

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuração do cliente AWS Lambda
lambda_client = boto3.client('lambda')

# Nome da função Lambda de geração de relatórios
REPORT_GENERATOR_FUNCTION = os.environ['REPORT_GENERATOR_FUNCTION']

def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attributes = event.get('sessionAttributes', {})

    if intent_name == 'GenerateReport':
        return handle_generate_report(slots, session_attributes)
    else:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, não entendi sua solicitação. Você pode tentar novamente?'
                }
            }
        }

def handle_generate_report(slots, session_attributes):
    report_type = slots['ReportType']
    
    if report_type not in ['diário', 'semanal']:
        return {
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': 'GenerateReport',
                'slots': slots,
                'slotToElicit': 'ReportType',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Por favor, especifique se você deseja um relatório diário ou semanal.'
                }
            }
        }
    
    try:
        response = lambda_client.invoke(
            FunctionName=REPORT_GENERATOR_FUNCTION,
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'report_type': 'daily' if report_type == 'diário' else 'weekly'
            })
        )
        
        result = json.loads(response['Payload'].read().decode())
        
        if result['statusCode'] == 200:
            return {
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',
                        'content': f'Seu relatório {report_type} foi gerado com sucesso. Você receberá um e-mail com o link para acessá-lo em breve.'
                    }
                }
            }
        else:
            raise Exception('Falha na geração do relatório')
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {str(e)}")
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Desculpe, ocorreu um erro ao gerar o relatório. Por favor, tente novamente mais tarde.'
                }
            }
        }