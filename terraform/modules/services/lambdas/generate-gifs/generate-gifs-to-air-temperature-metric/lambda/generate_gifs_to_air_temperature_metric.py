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
    temperature_levels = [-10, 0, 10, 20, 30, 40]  # Diferentes níveis de temperatura do ar em Celsius
    
    images = []
    for temp in temperature_levels:
        if temp < 0:
            condition = "Geada formando-se nas plantas. Ambiente congelado."
        elif temp < 10:
            condition = "Plantas com aspecto frio. Orvalho nas folhas."
        elif temp < 25:
            condition = "Plantas com aparência normal. Ambiente agradável."
        elif temp < 35:
            condition = "Plantas começando a murchar. Ar quente visível."
        else:
            condition = "Plantas murchando com calor extremo. Ondas de calor visíveis."
        
        prompt = f"Termômetro ao ar livre mostrando {temp}°C. {condition} Fundo com paisagem natural. Estilo fotorrealista."
        image = generate_image(prompt)
        images.append(image)
    
    # Criar o GIF
    gif_path = '/gif/air_temperature/air_temperature.gif'
    create_gif(images, gif_path)
    
    # Salvar o GIF em um bucket S3
    s3 = boto3.client('s3')
    bucket_name = 'air_temperature_media_bucket'
    
    with open(gif_path, 'rb') as gif_file:
        s3.put_object(Bucket=bucket_name, Key='air_temperature.gif', Body=gif_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps('GIF da temperatura do ar gerado e salvo com sucesso!')
    }