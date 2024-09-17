import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento de compartilhamento de conhecimento.
    """
    return knowledge_sharing_handler(event, context)

def knowledge_sharing_handler(event, context):
    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    knowledge_base = dynamodb.Table('KnowledgeBase')

    query = event['query']
    
    # Buscar soluções relevantes
    relevant_solutions = find_solutions(knowledge_base, query)

    return {
        'statusCode': 200,
        'body': json.dumps(relevant_solutions)
    }

def find_solutions(table, query):
    # Tokenizar a consulta
    tokens = query.lower().split()
    
    # Buscar soluções que correspondam a qualquer token da consulta
    response = table.scan(
        FilterExpression=Attr('keywords').contains(tokens[0]) |
                         Attr('problem').contains(tokens[0])
    )
    items = response['Items']

    # Continuar a busca para os tokens restantes
    for token in tokens[1:]:
        items = [item for item in items if token in item['keywords'] or token in item['problem'].lower()]

    # Ordenar os resultados por relevância (número de tokens correspondentes)
    items.sort(key=lambda x: sum(1 for token in tokens if token in x['keywords'] or token in x['problem'].lower()), reverse=True)

    # Limitar o número de resultados
    return items[:5]

def create_sample_data(table):
    # Função para criar dados de amostra na tabela DynamoDB
    sample_data = [
        {
            'id': '1',
            'problem': 'Pragas na soja',
            'solution': 'Uso de controle biológico com vespas Trichogramma',
            'keywords': ['soja', 'praga', 'controle biológico', 'vespa']
        },
        {
            'id': '2',
            'problem': 'Déficit hídrico em milho',
            'solution': 'Implementação de sistema de irrigação por gotejamento',
            'keywords': ['milho', 'seca', 'irrigação', 'gotejamento']
        },
        {
            'id': '3',
            'problem': 'Ferrugem asiática na soja',
            'solution': 'Aplicação preventiva de fungicidas e uso de variedades resistentes',
            'keywords': ['soja', 'ferrugem', 'fungicida', 'resistência']
        },
        {
            'id': '4',
            'problem': 'Compactação do solo em áreas de plantio direto',
            'solution': 'Rotação de culturas e uso de plantas de cobertura para descompactação biológica',
            'keywords': ['solo', 'compactação', 'plantio direto', 'rotação', 'cobertura']
        },
        {
            'id': '5',
            'problem': 'Baixa produtividade em café',
            'solution': 'Implementação de poda programada e adubação balanceada',
            'keywords': ['café', 'produtividade', 'poda', 'adubação']
        }
    ]

    with table.batch_writer() as batch:
        for item in sample_data:
            batch.put_item(Item=item)

# Descomente a linha abaixo para criar dados de amostra (execute apenas uma vez)
# create_sample_data(dynamodb.Table('KnowledgeBase'))