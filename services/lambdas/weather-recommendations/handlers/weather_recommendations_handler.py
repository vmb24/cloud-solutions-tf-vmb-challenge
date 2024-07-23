import json
import boto3
import subprocess
from uuid import uuid4
from datetime import datetime, timezone

class WeatherRecommendationsHandler:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('WeatherRecommendations')

    def get_jurassic2_response(self, prompt: str):
        cmd = [
            'aws', 'bedrock-runtime', 'invoke-model',
            '--model-id', 'jurassic-2-mid',
            '--content-type', 'application/json',
            '--accept', 'application/json',
            '--body', json.dumps({"prompt": prompt, "maxTokens": 512}),
            '--region', 'us-east-1'  # Ajuste para sua região
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        response_body = json.loads(result.stdout)
        return response_body['outputs'][0]['output']

    def generate_recommendations(self, query, context_data):
        prompt_template = """
        Você é um especialista em agricultura. Sua resposta final deverá ser um conjunto completo e detalhado de recomendações para otimizar a saúde e produção das plantas. 
        Utilize o contexto fornecido e o input do usuário para elaborar suas recomendações.
        Contexto: {context_data}
        Usuário: {query}
        Assistente:
        """
        
        full_prompt = prompt_template.format(context_data=context_data, query=query)
        response = self.get_jurassic2_response(full_prompt)
        return response
        
    def save_recommendation(self, query, context_data, recommendation):
        recommendation_id = str(uuid4())
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.table.put_item(
            Item={
                'recommendationId': recommendation_id,
                'query': query,
                'contextData': context_data,
                'recommendation': recommendation,
                'date': current_date
            }
        )
        return recommendation_id

    def get_response(self, query, context_data):
        recommendation = self.generate_recommendations(query, context_data)
        recommendation_id = self.save_recommendation(query, context_data, recommendation)
        return recommendation, recommendation_id

    def lambda_handler(self, event, context):
        soil_metric = event['soil_metric']
        climate_data = event['climate_data']
        query = f"Como otimizar a saúde e produção das plantas com base nas métricas de solo e clima?"

        context_data = f"Métricas do solo: pH={soil_metric['ph']}, Umidade={soil_metric['moisture']}, Temperatura={soil_metric['temperature']}. " \
                    f"Dados climáticos: Região={climate_data['region']}, Temperatura={climate_data['temperature']}, Umidade={climate_data['humidity']}."

        recommendation, recommendation_id = self.get_response(query, context_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recommendation': recommendation,
                'recommendation_id': recommendation_id
            })
        }
