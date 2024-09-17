import json
import boto3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do simulador de cenários.
    """
    return scenario_simulator_handler(event, context)

def scenario_simulator_handler(event, context):
    # Inicializar cliente de SageMaker
    sagemaker = boto3.client('sagemaker-runtime')

    scenario_params = event['scenario_params']
    
    # Simular cenário
    simulation_results = simulate_scenario(sagemaker, scenario_params)

    return {
        'statusCode': 200,
        'body': json.dumps(simulation_results)
    }

def simulate_scenario(sagemaker, params):
    # Preparar os dados para o modelo
    input_data = prepare_input_data(params)
    
    # Fazer previsões usando o modelo de Machine Learning
    predictions = make_predictions(sagemaker, input_data)
    
    # Calcular projeções e avaliação de risco
    yield_projection = predictions['yield']
    profit_projection = calculate_profit(yield_projection, params)
    risk_assessment = assess_risk(predictions['risk_score'])
    
    return {
        "yield_projection": yield_projection,
        "profit_projection": profit_projection,
        "risk_assessment": risk_assessment
    }

def prepare_input_data(params):
    # Converter parâmetros categóricos em numéricos
    crop_type_mapping = {'Milho': 0, 'Soja': 1, 'Trigo': 2}
    irrigation_type_mapping = {'Aspersão': 0, 'Gotejamento': 1, 'Superfície': 2}
    fertilizer_type_mapping = {'Orgânico': 0, 'Sintético': 1}
    pest_control_mapping = {'Biológico': 0, 'Químico': 1, 'Integrado': 2}
    
    input_data = [
        crop_type_mapping.get(params['crop_type'], -1),
        params['area_size'],
        irrigation_type_mapping.get(params['irrigation_type'], -1),
        fertilizer_type_mapping.get(params['fertilizer_type'], -1),
        pest_control_mapping.get(params['pest_control_method'], -1)
    ]
    
    # Normalizar os dados
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(np.array(input_data).reshape(1, -1))
    
    return input_data_scaled.tolist()[0]

def make_predictions(sagemaker, input_data):
    # Neste exemplo, vamos simular a chamada ao SageMaker
    # Em um cenário real, você faria uma chamada ao endpoint do seu modelo no SageMaker
    
    # Simulando um modelo de RandomForest para yield e risk score
    rf_yield = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_risk = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Dados de treinamento simulados
    X_train = np.random.rand(1000, 5)
    y_train_yield = np.random.rand(1000) * 10000  # yield entre 0 e 10000
    y_train_risk = np.random.rand(1000) * 100  # risk score entre 0 e 100
    
    rf_yield.fit(X_train, y_train_yield)
    rf_risk.fit(X_train, y_train_risk)
    
    yield_prediction = rf_yield.predict([input_data])[0]
    risk_score = rf_risk.predict([input_data])[0]
    
    return {
        'yield': round(yield_prediction, 2),
        'risk_score': round(risk_score, 2)
    }

def calculate_profit(yield_projection, params):
    # Lógica simplificada para cálculo de lucro
    # Em um cenário real, isso seria muito mais complexo
    base_price_per_kg = 2.5  # Preço base por kg
    cost_per_hectare = 1000  # Custo base por hectare
    
    revenue = yield_projection * base_price_per_kg
    cost = params['area_size'] * cost_per_hectare
    profit = revenue - cost
    
    return round(profit, 2)

def assess_risk(risk_score):
    if risk_score < 33:
        return "Baixo"
    elif risk_score < 66:
        return "Médio"
    else:
        return "Alto"