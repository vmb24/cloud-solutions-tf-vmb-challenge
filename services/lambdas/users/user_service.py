import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['resource']
    body = json.loads(event.get('body', '{}'))

    if path == '/users' and http_method == 'POST':
        return create_user(body)
    elif path.startswith('/users/') and http_method == 'GET':
        user_id = path.split('/')[-1]
        return get_user(user_id)
    elif path.startswith('/users/') and http_method == 'PUT':
        user_id = path.split('/')[-1]
        return update_user(user_id, body)
    elif path.startswith('/users/') and http_method == 'DELETE':
        user_id = path.split('/')[-1]
        return delete_user(user_id)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

def create_user(user_data):
    # Lógica para criar um usuário
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User created', 'user': user_data})
    }

def get_user(user_id):
    # Lógica para obter um usuário
    return {
        'statusCode': 200,
        'body': json.dumps({'user_id': user_id, 'user_data': {}})
    }

def update_user(user_id, user_data):
    # Lógica para atualizar um usuário
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User updated', 'user': user_data})
    }

def delete_user(user_id):
    # Lógica para excluir um usuário
    return {
        'statusCode': 204,
        'body': json.dumps({'message': 'User deleted'})
    }
