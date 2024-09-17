import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento do marketplace.
    """
    return marketplace_handler(event, context)

def marketplace_handler(event, context):
    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    products_table = dynamodb.Table('Products')
    user_needs_table = dynamodb.Table('UserNeeds')

    user_id = event['user_id']
    
    # Obter necessidades do usuário
    user_needs = get_user_needs(user_needs_table, user_id)

    # Buscar produtos relevantes
    relevant_products = find_relevant_products(products_table, user_needs)

    return {
        'statusCode': 200,
        'body': json.dumps(relevant_products)
    }

def get_user_needs(table, user_id):
    response = table.get_item(Key={'user_id': user_id})
    return response.get('Item', {})

def find_relevant_products(table, needs):
    # Extrair critérios de busca das necessidades do usuário
    product_type = needs.get('product_type', '')
    max_price = needs.get('max_price', 1000)
    preferred_brands = needs.get('preferred_brands', [])

    # Consulta base
    filter_expression = Attr('product_type').eq(product_type) & Attr('price').lte(max_price)

    # Adicionar filtro de marcas preferidas, se houver
    if preferred_brands:
        filter_expression &= Attr('brand').is_in(preferred_brands)

    # Realizar a consulta no DynamoDB
    response = table.scan(
        FilterExpression=filter_expression
    )

    # Processar e retornar os resultados
    relevant_products = response.get('Items', [])

    # Ordenar por relevância (neste caso, pelo preço mais baixo)
    relevant_products.sort(key=lambda x: x['price'])

    # Limitar a 5 produtos para não sobrecarregar o usuário
    return relevant_products[:5]