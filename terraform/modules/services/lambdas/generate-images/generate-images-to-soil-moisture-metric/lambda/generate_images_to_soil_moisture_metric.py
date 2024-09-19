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
    soil_moisture = event.get('soil_moisture', 50)  # Valor padrão de 50% se não for fornecido
    
    # 1. Imagens de culturas ideais
    if soil_moisture < 30:
        crop_prompt = "Culturas saudáveis resistentes à seca em solo seco, campo agrícola"
    elif soil_moisture < 60:
        crop_prompt = "Culturas verdes vibrantes em solo moderadamente úmido, campo agrícola"
    else:
        crop_prompt = "Culturas exuberantes prosperando em solo bem regado, campo agrícola"
    
    crop_image = generate_image(crop_prompt)
    
    # 2. Técnicas de irrigação recomendadas
    if soil_moisture < 30:
        irrigation_prompt = "Sistema eficiente de irrigação por gotejamento em ação, visão aproximada"
    elif soil_moisture < 60:
        irrigation_prompt = "Sistema de irrigação por aspersão regando culturas, visão ampla"
    else:
        irrigation_prompt = "Irrigação por inundação controlada em um campo nivelado"
    
    irrigation_image = generate_image(irrigation_prompt)
    
    # 3. Cobertura do solo adequada
    if soil_moisture < 30:
        mulch_prompt = "Camada espessa de cobertura orgânica protegendo a umidade do solo, visão aproximada"
    elif soil_moisture < 60:
        mulch_prompt = "Cobertura moderada de palha cobrindo o solo entre fileiras de culturas"
    else:
        mulch_prompt = "Cobertura vegetal leve protegendo a superfície do solo em um campo úmido"
    
    mulch_image = generate_image(mulch_prompt)
    
    # Salvar as imagens em um bucket S3 (assumindo que você tem permissões)
    s3 = boto3.client('s3')
    bucket_name = 'soil_moisture_media_bucket/images/soil_moisture'
    
    s3.put_object(Bucket=bucket_name, Key='crop_image.png', Body=crop_image)
    s3.put_object(Bucket=bucket_name, Key='irrigation_image.png', Body=irrigation_image)
    s3.put_object(Bucket=bucket_name, Key='mulch_image.png', Body=mulch_image)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Imagens geradas e salvas com sucesso!')
    }