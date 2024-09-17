import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do módulo de aprendizagem.
    """
    return learning_module_handler(event, context)

def learning_module_handler(event, context):
    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_progress_table = dynamodb.Table('UserProgress')
    modules_table = dynamodb.Table('LearningModules')

    user_id = event['user_id']
    
    # Obter progresso do usuário
    user_progress = user_progress_table.get_item(Key={'user_id': user_id}).get('Item', {})

    # Gerar próximo módulo de aprendizado
    next_module = generate_next_module(user_progress, modules_table)

    # Atualizar o progresso do usuário
    update_user_progress(user_progress_table, user_id, next_module['module_id'])

    return {
        'statusCode': 200,
        'body': json.dumps(next_module)
    }

def generate_next_module(progress, modules_table):
    completed_modules = progress.get('completed_modules', [])
    current_module = progress.get('current_module')

    # Se o usuário tiver um módulo atual, retorne-o
    if current_module:
        return get_module_by_id(modules_table, current_module)

    # Caso contrário, encontre o próximo módulo não completado
    all_modules = get_all_modules(modules_table)
    for module in all_modules:
        if module['module_id'] not in completed_modules:
            return module

    # Se todos os módulos foram completados, retorne o último
    return all_modules[-1] if all_modules else {"module_id": "END", "title": "Todos os módulos completados", "content": "Parabéns! Você completou todos os módulos disponíveis."}

def get_module_by_id(table, module_id):
    response = table.get_item(Key={'module_id': module_id})
    return response.get('Item', {})

def get_all_modules(table):
    response = table.scan()
    return sorted(response['Items'], key=lambda x: x['module_id'])

def update_user_progress(table, user_id, module_id):
    table.update_item(
        Key={'user_id': user_id},
        UpdateExpression="SET current_module = :m",
        ExpressionAttributeValues={':m': module_id}
    )

def create_sample_modules(table):
    # Função para criar dados de amostra na tabela DynamoDB
    sample_modules = [
        {
            'module_id': 'M001',
            'title': 'Introdução à Agricultura de Precisão',
            'content': 'Este módulo introduz os conceitos básicos da agricultura de precisão...'
        },
        {
            'module_id': 'M002',
            'title': 'Sensoriamento Remoto na Agricultura',
            'content': 'Aprenda como utilizar imagens de satélite e drones para monitorar suas culturas...'
        },
        {
            'module_id': 'M003',
            'title': 'Técnicas Avançadas de Irrigação',
            'content': 'Explore métodos modernos de irrigação para otimizar o uso da água...'
        },
        {
            'module_id': 'M004',
            'title': 'Manejo Integrado de Pragas',
            'content': 'Descubra estratégias sustentáveis para controle de pragas em suas plantações...'
        },
        {
            'module_id': 'M005',
            'title': 'Agricultura Digital e IoT',
            'content': 'Entenda como a Internet das Coisas está revolucionando a agricultura moderna...'
        }
    ]

    with table.batch_writer() as batch:
        for item in sample_modules:
            batch.put_item(Item=item)

# Descomente a linha abaixo para criar dados de amostra (execute apenas uma vez)
# create_sample_modules(dynamodb.Table('LearningModules'))