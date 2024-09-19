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
    air_temperature = event.get('air_temperature', 25)  # Valor padrão de 25°C se não for fornecido
    
    # 1. Imagens de plantas resistentes à temperatura atual do ar
    if air_temperature < 10:
        plant_prompt = "Plantas resistentes ao frio prosperando em ambiente de baixa temperatura, folhas robustas"
    elif air_temperature < 30:
        plant_prompt = "Plantas adaptadas a temperaturas moderadas, mostrando crescimento saudável em campo aberto"
    else:
        plant_prompt = "Plantas resistentes ao calor florescendo em ambiente de alta temperatura, folhas adaptadas"
    
    plant_image = generate_image(plant_prompt)
    
    # 2. Visualizações de estruturas de proteção (estufas, túneis, telas de sombreamento)
    if air_temperature < 10:
        protection_prompt = "Estufa fechada com sistema de aquecimento, protegendo plantas do frio extremo"
    elif air_temperature < 30:
        protection_prompt = "Túneis de plástico em campo agrícola, oferecendo proteção moderada contra variações de temperatura"
    else:
        protection_prompt = "Telas de sombreamento sobre culturas, protegendo plantas do calor intenso e da radiação solar"
    
    protection_image = generate_image(protection_prompt)
    
    # 3. Representações de técnicas de plantio adequadas para a temperatura (consórcio, rotação)
    if air_temperature < 10:
        planting_prompt = "Técnica de rotação de culturas de inverno, mostrando diferentes estágios de crescimento em campo frio"
    elif air_temperature < 30:
        planting_prompt = "Consórcio de plantas em clima temperado, exibindo diversidade de culturas em um mesmo campo"
    else:
        planting_prompt = "Técnica de plantio direto em ambiente quente, mostrando cobertura do solo e plantas resistentes ao calor"
    
    planting_image = generate_image(planting_prompt)
    
    # Salvar as imagens em um bucket S3 (assumindo que você tem permissões)
    s3 = boto3.client('s3')
    bucket_name = 'air_temperature_media_bucket/images/air_temperature'
    
    s3.put_object(Bucket=bucket_name, Key='air_temperature_plants.png', Body=plant_image)
    s3.put_object(Bucket=bucket_name, Key='temperature_protection.png', Body=protection_image)
    s3.put_object(Bucket=bucket_name, Key='planting_techniques.png', Body=planting_image)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Imagens relacionadas à temperatura do ar geradas e salvas com sucesso!')
    }