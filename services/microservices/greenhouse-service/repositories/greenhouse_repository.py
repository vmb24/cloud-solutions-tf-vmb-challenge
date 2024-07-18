import boto3
from models.greenhouse_metric import GreenhouseMetric, GreenhouseMetricCreate

class GreenhouseMetricRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('GreenhouseMetric')

    def create_greenhouse_metric(self, data: GreenhouseMetricCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item

    def get_greenhouse_metric(self, greenhouse_metric_id: str):
        response = self.table.get_item(Key={'id': greenhouse_metric_id})
        return response.get('Item')

    def update_greenhouse_metric(self, greenhouse_metric_id: str, data: GreenhouseMetricCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': greenhouse_metric_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_greenhouse_metric(self, greenhouse_metric_id: str):
        self.table.delete_item(Key={'id': greenhouse_metric_id})
