import boto3
from models.farmer import Farmer, FarmerCreate

class FarmerRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Farmers')

    def create_farmer(self, data: FarmerCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item

    def get_farmer(self, farmer_id: str):
        response = self.table.get_item(Key={'id': farmer_id})
        return response.get('Item')

    def update_farmer(self, farmer_id: str, data: FarmerCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': farmer_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_farmer(self, farmer_id: str):
        self.table.delete_item(Key={'id': farmer_id})
