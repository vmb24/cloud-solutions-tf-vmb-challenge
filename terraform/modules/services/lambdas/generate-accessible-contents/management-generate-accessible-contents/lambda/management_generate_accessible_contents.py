import json
import boto3
import os

# Inicializar clientes AWS
lambda_client = boto3.client('lambda')
step_functions_client = boto3.client('stepfunctions')

# ARNs das funções Lambda e da máquina de estado Step Functions
TEXT_TO_SPEECH_ARN = os.environ['TEXT_TO_SPEECH_ARN']
IMAGE_RECOGNITION_ARN = os.environ['IMAGE_RECOGNITION_ARN']
VIDEO_CAPTION_ARN = os.environ['VIDEO_CAPTION_ARN']
TEXT_SIMPLIFICATION_ARN = os.environ['TEXT_SIMPLIFICATION_ARN']
STEP_FUNCTION_ARN = os.environ['STEP_FUNCTION_ARN']

def lambda_handler(event, context):
    try:
        # Extrair o tipo de tarefa e os dados do evento
        task_type = event['type']
        data = event['data']
        
        if task_type == 'text_to_speech':
            response = invoke_lambda(TEXT_TO_SPEECH_ARN, data)
        elif task_type == 'image_recognition':
            response = invoke_lambda(IMAGE_RECOGNITION_ARN, data)
        elif task_type == 'video_caption':
            response = invoke_lambda(VIDEO_CAPTION_ARN, data)
        elif task_type == 'text_simplification':
            response = invoke_lambda(TEXT_SIMPLIFICATION_ARN, data)
        elif task_type == 'workflow':
            response = start_step_function(data)
        else:
            raise ValueError(f"Tipo de tarefa desconhecido: {task_type}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def invoke_lambda(function_arn, payload):
    response = lambda_client.invoke(
        FunctionName=function_arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.loads(response['Payload'].read())

def start_step_function(input_data):
    response = step_functions_client.start_execution(
        stateMachineArn=STEP_FUNCTION_ARN,
        input=json.dumps(input_data)
    )
    return {
        'executionArn': response['executionArn'],
        'startDate': str(response['startDate'])
    }