import json
import boto3
import base64

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
    light_data = event.get('light', {})
    light_status = light_data.get('status', 'Unknown')
    light_analog = light_data.get('analog', 0)
    
    # Classificação da intensidade de luz
    if light_status == "Unknown":
        light_condition = "desconhecida"
    elif light_analog == 0:
        light_condition = "muito baixa ou escuridão"
    elif light_analog < 500:
        light_condition = "baixa"
    elif light_analog < 800:
        light_condition = "moderada"
    else:
        light_condition = "alta"
    
    # 1. Imagens de culturas que se desenvolvem bem no nível atual de luminosidade
    crop_prompt = f"Plantas adaptadas a luz {light_condition} crescendo em ambiente agrícola, mostrando características típicas"
    crop_image = generate_image(crop_prompt)
    
    # 2. Visualizações de técnicas de manejo de luz
    if light_condition in ["desconhecida", "muito baixa ou escuridão", "baixa"]:
        light_management_prompt = "Sistema de iluminação artificial LED em estufa, fornecendo luz suplementar para plantas"
    elif light_condition == "moderada":
        light_management_prompt = "Combinação de luz natural e artificial em estufa, com telas de sombreamento parcialmente abertas"
    else:
        light_management_prompt = "Telas de sombreamento totalmente estendidas em estufa, protegendo plantas do excesso de luz solar"
    
    light_management_image = generate_image(light_management_prompt)
    
    # 3. Representações de disposições ideais de plantas para otimizar o uso da luz disponível
    if light_condition in ["desconhecida", "muito baixa ou escuridão", "baixa"]:
        plant_arrangement_prompt = "Disposição vertical de plantas em estufa para maximizar exposição à luz limitada, sistema de cultivo em camadas"
    elif light_condition == "moderada":
        plant_arrangement_prompt = "Arranjo escalonado de plantas em campo, com espécies mais altas ao fundo e mais baixas à frente"
    else:
        plant_arrangement_prompt = "Disposição espaçada de plantas em campo aberto para permitir penetração de luz, com plantas de sol pleno nos locais mais expostos"
    
    plant_arrangement_image = generate_image(plant_arrangement_prompt)
    
    # Salvar as imagens em um bucket S3 (assumindo que você tem permissões)
    s3 = boto3.client('s3')
    bucket_name = 'brightness_media_bucket/images/brightness'
    
    s3.put_object(Bucket=bucket_name, Key='light_adapted_crops.png', Body=crop_image)
    s3.put_object(Bucket=bucket_name, Key='light_management_techniques.png', Body=light_management_image)
    s3.put_object(Bucket=bucket_name, Key='optimal_plant_arrangement.png', Body=plant_arrangement_image)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Imagens relacionadas à luminosidade geradas e salvas com sucesso!')
    }