import boto3
from models.equipment_health import EquipmentHealth, EquipmentHealthCreate

class EquipmentHealthRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('EquipmentHealth')

    def create_equipment_health(self, data: EquipmentHealthCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item

    def get_equipment_health(self, equipment_health_id: str):
        response = self.table.get_item(Key={'id': equipment_health_id})
        return response.get('Item')

    def update_equipment_health(self, equipment_health_id: str, data: EquipmentHealthCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': equipment_health_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_equipment_health(self, equipment_health_id: str):
        self.table.delete_item(Key={'id': equipment_health_id})
