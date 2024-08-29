import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']

    if path == '/available_parking_spots' and http_method == 'GET':
        return list_available_parking_spots()
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def list_available_parking_spots():
    # Lógica para listar todas as vagas disponíveis
    return {
        'statusCode': 200,
        'body': json.dumps({'available_spots': []})
    }
