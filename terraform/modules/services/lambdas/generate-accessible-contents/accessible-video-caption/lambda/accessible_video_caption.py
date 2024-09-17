import boto3
import json
import time

def lambda_handler(event, context):
    transcribe_client = boto3.client('transcribe')
    
    job_name = f"TranscriptionJob_{context.aws_request_id}"
    bucket = event['bucket']
    video_key = event['video_key']
    
    job_uri = f"s3://{bucket}/{video_key}"
    
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='pt-BR',
        OutputBucketName=bucket
    )
    
    # Aguardar a conclusão do job (com timeout)
    for _ in range(30):  # Timeout após 5 minutos
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(10)
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return {
            'statusCode': 200,
            'body': json.dumps({'transcript_uri': transcript_uri})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Falha na transcrição')
        }