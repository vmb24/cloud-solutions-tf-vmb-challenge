import boto3
import json

def lambda_handler(event, context):
    polly_client = boto3.client('polly')
    s3_client = boto3.client('s3')
    
    text = event['text']
    language_code = event.get('language', 'pt-BR')
    
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Thiago',
        LanguageCode=language_code
    )
    
    # Salvar o áudio em um bucket S3
    bucket_name = 'seu-bucket-de-audio'
    file_name = f'audio_{context.aws_request_id}.mp3'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=response['AudioStream'].read()
    )
    
    audio_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    
    return {
        'statusCode': 200,
        'body': json.dumps({'audio_url': audio_url})
    }