import boto3
import json

def lambda_handler(event, context):
    comprehend_client = boto3.client('comprehend')
    
    text = event['text']
    
    # Extrair frases-chave
    response = comprehend_client.detect_key_phrases(
        Text=text,
        LanguageCode='pt'
    )
    
    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
    
    # Simplificar o texto usando as frases-chave
    simplified_text = "Pontos principais: " + ". ".join(key_phrases)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'simplified_text': simplified_text})
    }