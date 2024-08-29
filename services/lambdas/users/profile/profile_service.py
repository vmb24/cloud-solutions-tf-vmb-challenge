import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']
    body = json.loads(event.get('body', '{}'))

    if path.startswith('/profiles/') and http_method == 'GET':
        user_id = path.split('/')[-1]
        return get_profile(user_id)
    elif path.startswith('/profiles/') and http_method == 'PUT':
        user_id = path.split('/')[-1]
        return update_profile(user_id, body)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def get_profile(user_id):
    # Lógica para obter um perfil
    return {
        'statusCode': 200,
        'body': json.dumps({'user_id': user_id, 'profile': {}})
    }

def update_profile(user_id, profile_data):
    # Lógica para atualizar um perfil
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Profile updated', 'profile': profile_data})
    }
