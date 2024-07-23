import boto3
from models.soil_metric import SoilMetric, SoilMetricCreate

class SoilMetricsRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('SoilMetric')

    def create_soil_metric(self, data: SoilMetricCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item

    def get_soil_metric(self, soil_metric_id: str):
        response = self.table.get_item(Key={'id': soil_metric_id})
        return response.get('Item')

    def get_soil_metrics(self):
        response = self.table.scan()
        return response.get('Items', [])
    
    def update_soil_metric(self, soil_metric_id: str, data: SoilMetricCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': soil_metric_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_soil_metric(self, soil_metric_id: str):
        self.table.delete_item(Key={'id': soil_metric_id})
