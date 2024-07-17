import boto3
from boto3.dynamodb.conditions import Key

class GreenhouseRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Greenhouses')

    def create_greenhouse(self, data):
        self.table.put_item(Item=data)
        return data

    def get_greenhouse(self, greenhouse_id):
        response = self.table.get_item(Key={'GreenhouseID': greenhouse_id})
        return response.get('Item')

    def update_greenhouse(self, data):
        self.table.update_item(
            Key={'GreenhouseID': data['GreenhouseID']},
            UpdateExpression="set FarmerID = :f, Name = :n, Area = :a, Location = :l, Crops = :c, IrrigationSystems = :i",
            ExpressionAttributeValues={
                ':f': data['FarmerID'],
                ':n': data['Name'],
                ':a': data['Area'],
                ':l': data['Location'],
                ':c': data['Crops'],
                ':i': data['IrrigationSystems']
            },
            ReturnValues="UPDATED_NEW"
        )
        return data

    def delete_greenhouse(self, greenhouse_id):
        self.table.delete_item(Key={'GreenhouseID': greenhouse_id})
        return {'GreenhouseID': greenhouse_id}
