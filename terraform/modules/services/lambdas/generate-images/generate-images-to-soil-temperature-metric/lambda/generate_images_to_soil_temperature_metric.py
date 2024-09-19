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
    soil_temperature = event.get('soil_temperature', 20)  # Valor padrão de 20°C se não for fornecido
    
    # 1. Imagens de plantas que se desenvolvem bem na temperatura atual do solo
    if soil_temperature < 10:
        plant_prompt = "Plantas resistentes ao frio prosperando em solo frio, visão aproximada de raízes e folhas"
    elif soil_temperature < 25:
        plant_prompt = "Plantas de clima temperado crescendo em temperatura moderada do solo, mostrando sistema radicular saudável"
    else:
        plant_prompt = "Plantas tolerantes ao calor florescendo em solo quente, exibindo crescimento vigoroso"
    
    plant_image = generate_image(plant_prompt)
    
    # 2. Visualizações de técnicas de manejo do solo para regular a temperatura
    if soil_temperature < 10:
        management_prompt = "Camada espessa de cobertura orgânica isolando o solo do frio, visão aproximada"
    elif soil_temperature < 25:
        management_prompt = "Culturas de cobertura verde regulando a temperatura do solo em um campo, visão ampla"
    else:
        management_prompt = "Cobertura de cor clara refletindo a luz do sol para resfriar o solo, cenário agrícola"
    
    management_image = generate_image(management_prompt)
    
    # 3. Representações de sistemas de aquecimento/resfriamento do solo para estufas
    if soil_temperature < 10:
        greenhouse_prompt = "Sistema de aquecimento do solo de estufa com tubos, vista em corte transversal"
    elif soil_temperature < 25:
        greenhouse_prompt = "Design de estufa solar passiva para temperatura ideal do solo, vista em corte"
    else:
        greenhouse_prompt = "Sistema avançado de resfriamento de estufa para controle da temperatura do solo, diagrama esquemático"
    
    greenhouse_image = generate_image(greenhouse_prompt)
    
    # Salvar as imagens em um bucket S3 (assumindo que você tem permissões)
    s3 = boto3.client('s3')
    bucket_name = 'soil_temperature_media_bucket/images/soil_temperature'
    
    s3.put_object(Bucket=bucket_name, Key='plant_image.png', Body=plant_image)
    s3.put_object(Bucket=bucket_name, Key='management_image.png', Body=management_image)
    s3.put_object(Bucket=bucket_name, Key='greenhouse_image.png', Body=greenhouse_image)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Imagens relacionadas à temperatura do solo geradas e salvas com sucesso!')
    }