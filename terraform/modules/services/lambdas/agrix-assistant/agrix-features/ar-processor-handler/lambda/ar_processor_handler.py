import boto3
import json
import base64

# Inicializar o cliente Rekognition
rekognition_client = boto3.client('rekognition')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento AR.
    """
    return ar_processor_handler(event, context)

def ar_processor_handler(event, context):
    try:
        # Extrair a imagem do evento e decodificar de base64
        image_base64 = event['image']
        image_bytes = base64.b64decode(image_base64)
        
        # Analisar a imagem
        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes}
        )
        
        # Processar os resultados e criar informações sobrepostas
        overlays = []
        for label in response['Labels']:
            overlays.append({
                'label': label['Name'],
                'confidence': label['Confidence'],
                'position': 'center'  # Simplificado, você pode calcular posições baseadas em bounding boxes
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps(overlays)
        }
    except Exception as e:
        print(f"Erro no ar_processor_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao processar a imagem'})
        }