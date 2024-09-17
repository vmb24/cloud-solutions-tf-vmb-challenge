import json
import boto3
import numpy as np
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento de planejamento de cultivo.
    """
    return crop_planning_handler(event, context)

def crop_planning_handler(event, context):
    # Inicializar cliente de Machine Learning (SageMaker)
    sagemaker = boto3.client('sagemaker-runtime')

    farm_data = event['farm_data']
    
    # Usar modelo de ML para otimizar planejamento
    optimized_plan = optimize_crop_plan(sagemaker, farm_data)

    return {
        'statusCode': 200,
        'body': json.dumps(optimized_plan)
    }

def optimize_crop_plan(sagemaker, farm_data):
    # Preparar os dados para o modelo
    model_input = prepare_model_input(farm_data)

    # Invocar o modelo de ML
    response = sagemaker.invoke_endpoint(
        EndpointName='crop-planning-model',
        ContentType='application/json',
        Body=json.dumps(model_input)
    )

    # Processar a resposta do modelo
    result = json.loads(response['Body'].read().decode())

    # Interpretar os resultados e gerar o plano otimizado
    optimized_plan = interpret_model_output(result, farm_data)

    return optimized_plan

def prepare_model_input(farm_data):
    # Extrair e normalizar dados relevantes
    soil_type = farm_data.get('soil_type', 'unknown')
    climate_zone = farm_data.get('climate_zone', 'unknown')
    last_crops = farm_data.get('last_crops', [])
    area_size = farm_data.get('area_size', 0)

    # Codificar variáveis categóricas
    soil_type_encoded = encode_soil_type(soil_type)
    climate_zone_encoded = encode_climate_zone(climate_zone)
    last_crops_encoded = encode_last_crops(last_crops)

    return {
        'soil_type': soil_type_encoded,
        'climate_zone': climate_zone_encoded,
        'last_crops': last_crops_encoded,
        'area_size': area_size
    }

def interpret_model_output(model_output, farm_data):
    # Decodificar as previsões do modelo
    crop_rotation = decode_crops(model_output['predicted_crops'])
    planting_dates = generate_planting_dates(crop_rotation, farm_data['climate_zone'])
    expected_yield = calculate_expected_yield(model_output['yield_prediction'], farm_data['area_size'])
    recommendations = generate_recommendations(model_output, farm_data)

    return {
        'crop_rotation': crop_rotation,
        'planting_dates': planting_dates,
        'expected_yield': expected_yield,
        'recommendations': recommendations
    }

def encode_soil_type(soil_type):
    # Lógica de codificação do tipo de solo
    soil_types = {'arenoso': 0, 'argiloso': 1, 'siltoso': 2, 'humoso': 3}
    return soil_types.get(soil_type.lower(), 4)  # 4 para desconhecido

def encode_climate_zone(climate_zone):
    # Lógica de codificação da zona climática
    climate_zones = {'tropical': 0, 'subtropical': 1, 'temperado': 2, 'continental': 3}
    return climate_zones.get(climate_zone.lower(), 4)  # 4 para desconhecido

def encode_last_crops(last_crops):
    # Lógica de codificação das últimas culturas
    crop_codes = {'milho': 0, 'soja': 1, 'trigo': 2, 'algodão': 3, 'arroz': 4}
    return [crop_codes.get(crop.lower(), 5) for crop in last_crops]  # 5 para outros

def decode_crops(predicted_crops):
    # Lógica de decodificação das culturas previstas
    crop_names = ['Milho', 'Soja', 'Trigo', 'Algodão', 'Arroz']
    return [crop_names[i] for i in predicted_crops]

def generate_planting_dates(crop_rotation, climate_zone):
    # Lógica para gerar datas de plantio baseadas na rotação e zona climática
    base_date = datetime.now()
    dates = []
    for i, crop in enumerate(crop_rotation):
        if climate_zone.lower() == 'tropical':
            date = base_date + timedelta(days=i*120)  # Exemplo: 4 meses entre plantios
        else:
            date = base_date + timedelta(days=i*180)  # Exemplo: 6 meses entre plantios
        dates.append(date.strftime('%Y-%m-%d'))
    return dates

def calculate_expected_yield(yield_prediction, area_size):
    # Cálculo da produtividade esperada
    return round(yield_prediction * area_size, 2)

def generate_recommendations(model_output, farm_data):
    # Gerar recomendações baseadas na saída do modelo e dados da fazenda
    recommendations = []
    if model_output.get('irrigation_needed', False):
        recommendations.append("Considere implementar um sistema de irrigação para otimizar o rendimento.")
    if model_output.get('fertilizer_recommendation'):
        recommendations.append(f"Recomendação de fertilizante: {model_output['fertilizer_recommendation']}")
    if farm_data.get('soil_type') == 'arenoso':
        recommendations.append("Considere técnicas de conservação do solo para melhorar a retenção de água.")
    return recommendations