import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

step_functions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    try:
        # Extrair parâmetros relevantes do evento
        slots = event['currentIntent']['slots']
        session_attributes = event.get('sessionAttributes', {})

        # Iniciar execução do Step Functions
        response = step_functions_client.start_execution(
            stateMachineArn=os.environ['SOIL_MOISTURE_WORKFLOW_ARN'],
            input=json.dumps({
                'slots': slots,
                'sessionAttributes': session_attributes
            })
        )

        # Aguardar a conclusão da execução do Step Functions
        execution_arn = response['executionArn']
        while True:
            execution_status = step_functions_client.describe_execution(executionArn=execution_arn)
            if execution_status['status'] == 'SUCCEEDED':
                break
            elif execution_status['status'] in ['FAILED', 'TIMED_OUT', 'ABORTED']:
                raise Exception(f"Step Functions execution failed: {execution_status['status']}")

        # Obter o resultado da execução
        result = json.loads(execution_status['output'])

        # Formatar a resposta para o usuário
        moisture_level = result.get('moistureLevel', 'N/A')
        recommendations = result.get('recommendations', [])
        tasks = result.get('tasks', [])

        response_content = (
            f"Com base na nossa análise, o nível de umidade do solo é {moisture_level}. "
            f"Recomendações: {'; '.join(recommendations)}. "
            f"Tarefas sugeridas: {'; '.join(tasks)}."
        )

        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': response_content
                }
            }
        }

    except Exception as e:
        logger.error(f"Erro em soil_moisture_fulfillment: {str(e)}")
        return {
            'sessionAttributes': event.get('sessionAttributes', {}),
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': "Desculpe, ocorreu um erro ao processar as informações de umidade do solo. Por favor, tente novamente mais tarde."
                }
            }
        }