import json
import boto3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do assistente de sustentabilidade.
    """
    return sustainability_assistant_handler(event, context)

def sustainability_assistant_handler(event, context):
    # Inicializar cliente de SageMaker
    sagemaker = boto3.client('sagemaker-runtime')

    farm_practices = event['farm_practices']
    
    # Analisar práticas atuais e gerar recomendações
    sustainability_analysis = analyze_sustainability(sagemaker, farm_practices)

    return {
        'statusCode': 200,
        'body': json.dumps(sustainability_analysis)
    }

def analyze_sustainability(sagemaker, practices):
    # Preparar os dados para o modelo
    input_data = prepare_input_data(practices)
    
    # Fazer previsões usando o modelo de Machine Learning
    sustainability_score = predict_sustainability_score(sagemaker, input_data)
    
    # Gerar recomendações com base nas práticas atuais
    recommendations = generate_recommendations(practices, sustainability_score)
    
    return {
        "score": sustainability_score,
        "recommendations": recommendations
    }

def prepare_input_data(practices):
    # Converter práticas categóricas em numéricas
    irrigation_mapping = {'Gotejamento': 2, 'Aspersão': 1, 'Superfície': 0}
    fertilizer_mapping = {'Orgânico': 2, 'Misto': 1, 'Químico': 0}
    pest_control_mapping = {'Integrado': 2, 'Biológico': 1, 'Químico': 0}
    soil_management_mapping = {'Conservação': 2, 'Mínimo': 1, 'Convencional': 0}
    crop_rotation_mapping = {'Yes': 1, 'No': 0}
    
    input_data = [
        irrigation_mapping.get(practices['irrigation_method'], -1),
        fertilizer_mapping.get(practices['fertilizer_use'], -1),
        pest_control_mapping.get(practices['pest_control'], -1),
        soil_management_mapping.get(practices['soil_management'], -1),
        crop_rotation_mapping.get(practices['crop_rotation'], -1)
    ]
    
    # Normalizar os dados
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(np.array(input_data).reshape(1, -1))
    
    return input_data_scaled.tolist()[0]

def predict_sustainability_score(sagemaker, input_data):
    # Neste exemplo, vamos simular a chamada ao SageMaker
    # Em um cenário real, você faria uma chamada ao endpoint do seu modelo no SageMaker
    
    # Simulando um modelo de RandomForest para o score de sustentabilidade
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Dados de treinamento simulados
    X_train = np.random.rand(1000, 5)
    y_train = np.random.rand(1000) * 100  # score entre 0 e 100
    
    rf_model.fit(X_train, y_train)
    
    score_prediction = rf_model.predict([input_data])[0]
    
    return round(score_prediction, 2)

def generate_recommendations(practices, score):
    recommendations = []
    
    if practices['irrigation_method'] != 'Gotejamento':
        recommendations.append("Considere implementar um sistema de irrigação por gotejamento para melhorar a eficiência do uso da água.")
    
    if practices['fertilizer_use'] != 'Orgânico':
        recommendations.append("Aumente o uso de fertilizantes orgânicos para melhorar a saúde do solo a longo prazo.")
    
    if practices['pest_control'] != 'Integrado':
        recommendations.append("Implemente um sistema de manejo integrado de pragas para reduzir a dependência de pesticidas químicos.")
    
    if practices['soil_management'] != 'Conservação':
        recommendations.append("Adote práticas de conservação do solo, como plantio direto e uso de cobertura vegetal.")
    
    if practices['crop_rotation'] == 'No':
        recommendations.append("Implemente um sistema de rotação de culturas para melhorar a saúde do solo e reduzir problemas com pragas e doenças.")
    
    if score < 50:
        recommendations.append("Considere buscar orientação de um especialista em agricultura sustentável para desenvolver um plano abrangente de melhoria.")
    
    return recommendations[:5]  # Retorna no máximo 5 recomendações