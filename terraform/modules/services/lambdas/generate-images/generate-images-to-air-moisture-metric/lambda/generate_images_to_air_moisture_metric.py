import json
import boto3
import base64
import os

# Inicialize o cliente Bedrock
bedrock = boto3.client(service_name='bedrock-runtime')

def generate_image(prompt):
    body = json.dumps({
        "modelId": "stability.stable-diffusion-xl-v0",
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt,
            "negativeText": "low quality, blurry",
            "height": 512,
            "width": 512,
            "cfgScale": 7,
            "seed": 0,
            "steps": 50,
            "style": "photographic"
        }
    })

    response = bedrock.invoke_model(body=body, modelId="stability.stable-diffusion-xl-v0", contentType="application/json", accept="application/json")
    response_body = json.loads(response.get('body').read())
    
    return base64.b64decode(response_body['images'][0])

def lambda_handler(event, context):
    air_humidity = event.get('air_humidity', 50)  # Valor padrão de 50% se não for fornecido
    
    # 1. Imagens de culturas adaptadas às condições atuais de umidade do ar
    if air_humidity < 30:
        crop_prompt = "Culturas resistentes à seca prosperando em ambiente de baixa umidade, campo agrícola"
    elif air_humidity < 70:
        crop_prompt = "Diversas culturas crescendo bem em condições de umidade moderada, campo verde exuberante"
    else:
        crop_prompt = "Plantas tropicais florescendo em ambiente de alta umidade, folhagem densa"
    
    crop_image = generate_image(crop_prompt)
    
    # 2. Visualizações de técnicas para controle de umidade
    if air_humidity < 30:
        humidity_control_prompt = "Sistema de nebulização em ação, finas gotículas de água no ar, ambiente de estufa"
    elif air_humidity < 70:
        humidity_control_prompt = "Sistema de ventilação equilibrado em uma estufa, ventiladores e aberturas visíveis"
    else:
        humidity_control_prompt = "Sistema de desumidificação operando em uma estufa, umidade sendo removida"
    
    humidity_control_image = generate_image(humidity_control_prompt)
    
    # 3. Representações de estruturas de proteção contra excesso ou falta de umidade
    if air_humidity < 30:
        protection_prompt = "Estufa fechada com sistemas de retenção de umidade, vista interior nebulosa"
    elif air_humidity < 70:
        protection_prompt = "Estufa de laterais abertas com painéis ajustáveis, permitindo controle do fluxo de ar"
    else:
        protection_prompt = "Estufa com sistema avançado de desumidificação e circulação de ar, diagrama técnico"
    
    protection_image = generate_image(protection_prompt)
    
    # Salvar as imagens em um bucket S3 (assumindo que você tem permissões)
    s3 = boto3.client('s3')
    bucket_name = 'air_moisture_media_bucket/images/air_moisture'
    
    s3.put_object(Bucket=bucket_name, Key='air_humidity_crop.png', Body=crop_image)
    s3.put_object(Bucket=bucket_name, Key='humidity_control.png', Body=humidity_control_image)
    s3.put_object(Bucket=bucket_name, Key='humidity_protection.png', Body=protection_image)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Imagens relacionadas à umidade do ar geradas e salvas com sucesso!')
    }