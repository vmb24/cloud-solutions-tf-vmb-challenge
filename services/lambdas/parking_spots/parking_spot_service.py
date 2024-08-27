import json
import boto3
from botocore.exceptions import ClientError

# Inicialize o cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingSpots')  # Substitua 'ParkingSpots' pelo nome real da sua tabela

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']
    body = json.loads(event.get('body', '{}'))

    if path.startswith('/parking_spots/') and http_method == 'GET':
        spot_id = path.split('/')[-1]
        return get_parking_spot(spot_id)
    elif path == '/parking_spots' and http_method == 'POST':
        return create_parking_spot(body)
    elif path == '/parking_spots' and http_method == 'GET':
        return list_parking_spots()
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def get_parking_spot(spot_id):
    try:
        response = table.get_item(
            Key={'spot_id': spot_id}
        )
        item = response.get('Item')
        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Parking spot not found'})
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_parking_spot(spot_data):
    spot_id = spot_data.get('spot_id')
    try:
        table.put_item(
            Item=spot_data
        )
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Parking spot created', 'spot': spot_data})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def list_parking_spots():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps({'parking_spots': items})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
