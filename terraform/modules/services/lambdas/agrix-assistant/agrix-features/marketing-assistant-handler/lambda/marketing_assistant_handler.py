import json
import boto3
import random

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do assistente de marketing.
    """
    return marketing_assistant_handler(event, context)

def marketing_assistant_handler(event, context):
    # Inicializar cliente de Machine Learning (por exemplo, SageMaker)
    sagemaker = boto3.client('sagemaker-runtime')

    product_data = event['product_data']
    
    # Prever preços e demanda
    market_analysis = analyze_market(sagemaker, product_data)

    return {
        'statusCode': 200,
        'body': json.dumps(market_analysis)
    }

def analyze_market(sagemaker, product_data):
    # Aqui você normalmente faria uma chamada para um endpoint do SageMaker
    # Para este exemplo, vamos simular a análise

    # Simular previsão de preço
    base_price = 5.0
    price_factors = {
        'Frutas': 0.8,
        'Verduras': 0.7,
        'Grãos': 1.2,
        'Processados': 1.5
    }
    price_factor = price_factors.get(product_data['product_type'], 1.0)
    predicted_price = base_price * price_factor * random.uniform(0.9, 1.1)

    # Simular previsão de demanda
    demand_options = ['Baixa', 'Média', 'Alta']
    demand_weights = [0.2, 0.5, 0.3]
    demand_forecast = random.choices(demand_options, weights=demand_weights)[0]

    # Simular melhores mercados
    all_markets = ['Mercado Central', 'Feira Orgânica', 'Supermercado Local', 'Mercado Online']
    best_markets = random.sample(all_markets, k=random.randint(2, 3))

    return {
        "predicted_price": round(predicted_price, 2),
        "demand_forecast": demand_forecast,
        "best_markets": best_markets
    }

# Função para simular uma chamada ao SageMaker (não utilizada no exemplo acima)
def invoke_sagemaker_endpoint(sagemaker, endpoint_name, input_data):
    response = sagemaker.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(input_data)
    )
    result = json.loads(response['Body'].read().decode())
    return result