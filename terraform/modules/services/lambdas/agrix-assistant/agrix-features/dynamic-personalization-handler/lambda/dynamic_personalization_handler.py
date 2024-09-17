import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento de personalização dinâmica.
    """
    return dynamic_personalization_handler(event, context)

def dynamic_personalization_handler(event, context):
    # Inicializar cliente DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserPreferences')

    user_id = event['user_id']
    
    # Obter preferências do usuário
    response = table.get_item(Key={'user_id': user_id})
    user_preferences = response.get('Item', {})

    # Personalizar conteúdo baseado nas preferências
    personalized_content = personalize_content(user_preferences)

    # Atualizar as estatísticas de uso
    update_user_statistics(table, user_id)

    return {
        'statusCode': 200,
        'body': json.dumps(personalized_content)
    }

def personalize_content(preferences):
    content = "Conteúdo personalizado baseado nas suas preferências:\n"
    recommendations = []
    custom_message = ""

    # Personalização baseada em interesses
    if 'interests' in preferences:
        interests = preferences['interests']
        content += f"Seus interesses principais são: {', '.join(interests)}\n"
        recommendations.extend(get_recommendations_by_interests(interests))

    # Personalização baseada no nível de experiência
    if 'experience_level' in preferences:
        exp_level = preferences['experience_level']
        content += f"Conteúdo adaptado para seu nível de experiência: {exp_level}\n"
        recommendations.extend(get_recommendations_by_experience(exp_level))

    # Personalização baseada no histórico de interações
    if 'interaction_history' in preferences:
        interaction_history = preferences['interaction_history']
        custom_message = generate_custom_message(interaction_history)

    return {
        "content": content,
        "recommendations": recommendations,
        "custom_message": custom_message
    }

def get_recommendations_by_interests(interests):
    # Simulação de recomendações baseadas em interesses
    recommendations = []
    interest_recommendations = {
        "tecnologia": "Confira nossos últimos artigos sobre IA e Machine Learning",
        "esportes": "Veja os destaques dos jogos de ontem",
        "culinária": "Novas receitas de pratos saudáveis para você experimentar",
        "viagens": "Descubra os destinos mais populares para suas próximas férias"
    }
    for interest in interests:
        if interest in interest_recommendations:
            recommendations.append(interest_recommendations[interest])
    return recommendations

def get_recommendations_by_experience(exp_level):
    # Simulação de recomendações baseadas no nível de experiência
    recommendations = {
        "iniciante": "Comece com nossos tutoriais básicos para iniciantes",
        "intermediário": "Explore nossos cursos avançados para aprimorar suas habilidades",
        "avançado": "Confira nossos desafios técnicos para profissionais experientes"
    }
    return [recommendations.get(exp_level, "Explore nosso conteúdo variado")]

def generate_custom_message(interaction_history):
    # Gerar mensagem personalizada com base no histórico de interações
    interaction_count = len(interaction_history)
    if interaction_count == 0:
        return "Bem-vindo! Estamos felizes em tê-lo conosco."
    elif interaction_count < 5:
        return f"Obrigado por usar nosso serviço! Esta é sua {interaction_count}ª interação."
    else:
        return "Agradecemos sua fidelidade! Temos novidades especiais para usuários frequentes como você."

def update_user_statistics(table, user_id):
    # Atualizar estatísticas de uso do usuário
    table.update_item(
        Key={'user_id': user_id},
        UpdateExpression="SET interaction_count = if_not_exists(interaction_count, :start) + :inc",
        ExpressionAttributeValues={
            ':inc': 1,
            ':start': 0
        }
    )