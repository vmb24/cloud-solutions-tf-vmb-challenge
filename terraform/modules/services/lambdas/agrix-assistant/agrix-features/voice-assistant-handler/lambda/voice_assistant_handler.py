import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do assistente de voz.
    """
    return voice_assistant_handler(event, context)

def voice_assistant_handler(event, context):
    # Inicializar o cliente Polly e S3
    polly_client = boto3.client('polly')
    s3_client = boto3.client('s3')
    
    # Extrair a mensagem do evento
    message = event['message']
    
    try:
        # Converter texto em fala
        response = polly_client.synthesize_speech(
            Text=message,
            OutputFormat='mp3',
            VoiceId='Ricardo'  # Voz masculina em português brasileiro
        )
        
        # Gerar um nome único para o arquivo de áudio
        audio_filename = f"agrix_voice_{context.aws_request_id}.mp3"
        
        # Salvar o áudio em um bucket S3
        s3_bucket = os.environ['S3_BUCKET_NAME']
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=audio_filename,
            Body=response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )
        
        # Gerar URL pré-assinada para o áudio
        audio_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket, 'Key': audio_filename},
            ExpiresIn=3600  # URL válida por 1 hora
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'audio_url': audio_url})
        }
    except ClientError as e:
        print(f"Erro ao processar a solicitação de voz: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao gerar áudio')
        }