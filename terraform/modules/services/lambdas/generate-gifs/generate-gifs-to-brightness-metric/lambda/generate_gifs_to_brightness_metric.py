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
    light_levels = ["amanhecer", "manhã", "meio-dia", "tarde", "pôr do sol", "noite"]
    
    images_sun = []
    images_greenhouse = []
    
    for level in light_levels:
        if level == "amanhecer":
            sun_condition = "Sol nascendo no horizonte. Céu com tons alaranjados."
            greenhouse_condition = "Lâmpadas de crescimento começando a ligar. Luz fraca."
            plant_state = "Planta começando a despertar."
        elif level == "manhã":
            sun_condition = "Sol baixo no céu. Luz suave da manhã."
            greenhouse_condition = "Lâmpadas de crescimento totalmente ligadas. Luz moderada."
            plant_state = "Planta se abrindo para a luz."
        elif level == "meio-dia":
            sun_condition = "Sol alto no céu. Luz intensa do meio-dia."
            greenhouse_condition = "Lâmpadas de crescimento em intensidade máxima."
            plant_state = "Planta totalmente aberta, crescendo vigorosamente."
        elif level == "tarde":
            sun_condition = "Sol começando a descer. Luz dourada da tarde."
            greenhouse_condition = "Lâmpadas de crescimento começando a diminuir intensidade."
            plant_state = "Planta ainda ativa, mas começando a se preparar para a noite."
        elif level == "pôr do sol":
            sun_condition = "Sol se pondo no horizonte. Céu com tons avermelhados."
            greenhouse_condition = "Lâmpadas de crescimento em baixa intensidade."
            plant_state = "Planta começando a fechar suas folhas."
        else:  # noite
            sun_condition = "Céu escuro com estrelas. Lua visível."
            greenhouse_condition = "Lâmpadas de crescimento desligadas."
            plant_state = "Planta em repouso noturno."

        prompt_sun = f"Paisagem natural com {sun_condition} {plant_state} Estilo fotorrealista."
        prompt_greenhouse = f"Interior de estufa com {greenhouse_condition} {plant_state} Estilo fotorrealista."

        image_sun = generate_image(prompt_sun)
        image_greenhouse = generate_image(prompt_greenhouse)

        images_sun.append(image_sun)
        images_greenhouse.append(image_greenhouse)
    
    # Criar os GIFs
    gif_path_sun = '/gif/sun_luminosity/sun_luminosity.gif'
    gif_path_greenhouse = '/gif/greenhouse_luminosity/greenhouse_luminosity.gif'
    create_gif(images_sun, gif_path_sun)
    create_gif(images_greenhouse, gif_path_greenhouse)
    
    # Salvar os GIFs em um bucket S3
    s3 = boto3.client('s3')
    bucket_name = 'brightness_media_bucket'
    
    with open(gif_path_sun, 'rb') as gif_file:
        s3.put_object(Bucket=bucket_name, Key='sun_luminosity.gif', Body=gif_file)
    
    with open(gif_path_greenhouse, 'rb') as gif_file:
        s3.put_object(Bucket=bucket_name, Key='greenhouse_luminosity.gif', Body=gif_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps('GIFs de luminosidade (sol e estufa) gerados e salvos com sucesso!')
    }