import json
import subprocess
import boto3
from models.soil_metric import SoilMetric, SoilMetricCreate
from repositories.soil_metrics_repository import SoilMetricsRepository

class SoilMetricsUsecase:
    def __init__(self):
        self.repo = SoilMetricsRepository()
        self.bedrock_client = boto3.client('bedrock-runtime')

    def create_soil_metric(self, data: SoilMetricCreate):
        soil_metric = self.repo.create_soil_metric(data)
        recommendation = self.get_recommendation(soil_metric)
        return {**soil_metric.dict(), "recommendation": recommendation}

    def get_soil_metric(self, soil_metric_id: str):
        soil_metric = self.repo.get_soil_metric(soil_metric_id)
        recommendation = self.get_recommendation(soil_metric)
        return {**soil_metric.dict(), "recommendation": recommendation}

    def get_soil_metrics(self):
        soil_metrics = self.repo.get_soil_metrics()
        return [{"soil_metric": sm.dict(), "recommendation": self.get_recommendation(sm)} for sm in soil_metrics]
    
    def update_soil_metric(self, soil_metric_id: str, data: SoilMetricCreate):
        return self.repo.update_soil_metric(soil_metric_id, data)

    def delete_soil_metric(self, soil_metric_id: str):
        return self.repo.delete_soil_metric(soil_metric_id)

    def get_recommendation(self, soil_metric: SoilMetric):
        prompt_template = """
        Você é um especialista em agricultura. Sua resposta final deverá ser um conjunto completo e detalhado de recomendações para otimizar a saúde e produção das plantas. 
        Utilize o contexto fornecido e o input do usuário para elaborar suas recomendações.
        Contexto: {context_data}
        Usuário: {query}
        Assistente:
        """
        
        full_prompt = prompt_template.format(
            context_data=f"pH: {soil_metric.ph_level}, Umidade: {soil_metric.moisture_level}, Temperatura: {soil_metric.temperature}",
            query="Como posso otimizar a saúde e produção das plantas com base nas métricas fornecidas?"
        )
        
        response = self.get_jurassic2_response(full_prompt)
        return response

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
