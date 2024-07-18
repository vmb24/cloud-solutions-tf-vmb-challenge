import boto3
from models.crop_health import CropHealth, CropHealthCreate

class CropHealthRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CropHealth')

    def create_crop_health(self, data: CropHealthCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item

    def get_crop_health(self, crop_health_id: str):
        response = self.table.get_item(Key={'id': crop_health_id})
        return response.get('Item')

    def update_crop_health(self, crop_health_id: str, data: CropHealthCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': crop_health_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_crop_health(self, crop_health_id: str):
        self.table.delete_item(Key={'id': crop_health_id})
