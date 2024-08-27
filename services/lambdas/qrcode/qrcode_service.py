import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']
    body = json.loads(event.get('body', '{}'))

    if path == '/qrcodes' and http_method == 'POST':
        return generate_qr_code(body)
    elif path.startswith('/qrcodes/') and http_method == 'GET':
        qr_code_id = path.split('/')[-1]
        return validate_qr_code(qr_code_id)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def generate_qr_code(qr_data):
    # Lógica para gerar QR Code
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'QR Code generated', 'qr_code': qr_data})
    }

def validate_qr_code(qr_code_id):
    # Lógica para validar QR Code
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'QR Code validated', 'qr_code_id': qr_code_id})
    }
