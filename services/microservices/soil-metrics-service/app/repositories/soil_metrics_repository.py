import boto3
from boto3.dynamodb.conditions import Key

class SoilMetricsRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('SoilMetrics')

    def create_soil_metric(self, data):
        self.table.put_item(Item=data)
        return data

    def get_soil_metric(self, metric_id):
        response = self.table.get_item(Key={'MetricID': metric_id})
        return response.get('Item')

    def update_soil_metric(self, data):
        self.table.update_item(
            Key={'MetricID': data['MetricID']},
            UpdateExpression="set FarmerID = :f, PH = :p, Moisture = :m, Temperature = :t, Timestamp = :ts",
            ExpressionAttributeValues={
                ':f': data['FarmerID'],
                ':p': data['PH'],
                ':m': data['Moisture'],
                ':t': data['Temperature'],
                ':ts': data['Timestamp']
            },
            ReturnValues="UPDATED_NEW"
        )
        return data

    def delete_soil_metric(self, metric_id):
        self.table.delete_item(Key={'MetricID': metric_id})
        return {'MetricID': metric_id}
