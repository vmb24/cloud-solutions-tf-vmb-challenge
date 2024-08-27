import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']
    body = json.loads(event.get('body', '{}'))

    if path == '/reservations' and http_method == 'POST':
        return create_reservation(body)
    elif path.startswith('/reservations/') and http_method == 'GET':
        reservation_id = path.split('/')[-1]
        return get_reservation(reservation_id)
    elif path.startswith('/reservations/') and http_method == 'PUT':
        reservation_id = path.split('/')[-1]
        return update_reservation_status(reservation_id, body)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def create_reservation(reservation_data):
    # Lógica para criar uma nova reserva
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Reservation created', 'reservation': reservation_data})
    }

def get_reservation(reservation_id):
    # Lógica para obter detalhes sobre uma reserva específica
    return {
        'statusCode': 200,
        'body': json.dumps({'reservation_id': reservation_id, 'reservation_data': {}})
    }

def update_reservation_status(reservation_id, status_data):
    # Lógica para atualizar o status de uma reserva existente
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Reservation status updated', 'status': status_data})
    }
