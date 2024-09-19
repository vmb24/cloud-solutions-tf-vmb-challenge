import json
import boto3
import base64
import os
from PIL import Image
import io

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

def create_gif(images, output_path):
    frames = [Image.open(io.BytesIO(img)) for img in images]
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000, loop=0)

def lambda_handler(event, context):
    moisture_levels = [10, 30, 50, 70, 90]  # Diferentes níveis de umidade do ar em porcentagem
    
    images = []
    for moisture in moisture_levels:
        if moisture < 30:
            condition = "seco"
            drops = "sem gotas de água no ar"
        elif moisture < 60:
            condition = "moderado"
            drops = "poucas gotas de água no ar"
        else:
            condition = "úmido"
            drops = "muitas gotas de água no ar"
        
        prompt = f"Higrômetro simples mostrando {moisture}% de umidade do ar. Ponteiro entre 'seco' e 'úmido' apontando para {condition}. {drops}. Fundo claro. Estilo fotorrealista."
        image = generate_image(prompt)
        images.append(image)
    
    # Criar o GIF
    gif_path = '/gif/air_moisture/air_moisture.gif'
    create_gif(images, gif_path)
    
    # Salvar o GIF em um bucket S3
    s3 = boto3.client('s3')
    bucket_name = 'air_moisture_media_bucket'
    
    with open(gif_path, 'rb') as gif_file:
        s3.put_object(Bucket=bucket_name, Key='air_moisture.gif', Body=gif_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps('GIF da umidade do ar gerado e salvo com sucesso!')
    }