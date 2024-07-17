import boto3
from boto3.dynamodb.conditions import Key

class FarmerRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Farmers')

    def create_farmer(self, data):
        self.table.put_item(Item=data)
        return data

    def get_farmer(self, farmer_id):
        response = self.table.get_item(Key={'FarmerID': farmer_id})
        return response.get('Item')

    def update_farmer(self, data):
        self.table.update_item(
            Key={'FarmerID': data['FarmerID']},
            UpdateExpression="set Name = :n, Email = :e, Address = :a, PhoneNumber = :p, ProfileImage = :pi",
            ExpressionAttributeValues={
                ':n': data['Name'],
                ':e': data['Email'],
                ':a': data['Address'],
                ':p': data['PhoneNumber'],
                ':pi': data['ProfileImage']
            },
            ReturnValues="UPDATED_NEW"
        )
        return data

    def delete_farmer(self, farmer_id):
        self.table.delete_item(Key={'FarmerID': farmer_id})
        return {'FarmerID': farmer_id}
