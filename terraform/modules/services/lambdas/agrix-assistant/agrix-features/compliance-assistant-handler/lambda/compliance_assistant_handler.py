import json
import boto3

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento de conformidade.
    """
    return compliance_assistant_handler(event, context)

def compliance_assistant_handler(event, context):
    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    regulations_table = dynamodb.Table('Regulations')

    farm_practices = event['farm_practices']
    
    # Verificar conformidade
    compliance_check = check_compliance(regulations_table, farm_practices)

    return {
        'statusCode': 200,
        'body': json.dumps(compliance_check)
    }

def check_compliance(table, practices):
    compliance_issues = []
    recommendations = []

    # Buscar todas as regulamentações aplicáveis
    response = table.scan()
    regulations = response['Items']

    for regulation in regulations:
        if not is_compliant(practices, regulation):
            compliance_issues.append(regulation['name'])
            recommendations.append(get_recommendation(regulation))

    is_compliant = len(compliance_issues) == 0

    return {
        "compliant": is_compliant,
        "compliance_issues": compliance_issues,
        "recommendations": recommendations
    }

def is_compliant(practices, regulation):
    # Lógica para verificar se as práticas estão em conformidade com a regulamentação
    if regulation['type'] == 'pesticide_usage':
        return practices.get('pesticide_usage', '') in regulation['allowed_pesticides']
    elif regulation['type'] == 'water_management':
        return practices.get('water_usage', 0) <= regulation['max_water_usage']
    # Adicione mais verificações conforme necessário
    return True

def get_recommendation(regulation):
    if regulation['type'] == 'pesticide_usage':
        return f"Utilize apenas pesticidas aprovados: {', '.join(regulation['allowed_pesticides'])}"
    elif regulation['type'] == 'water_management':
        return f"Reduza o uso de água para no máximo {regulation['max_water_usage']} litros por hectare"
    # Adicione mais recomendações conforme necessário
    return "Revise suas práticas para atender às regulamentações"