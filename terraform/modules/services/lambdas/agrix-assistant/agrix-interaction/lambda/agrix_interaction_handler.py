import json
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Certifique-se de baixar os recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Dicionário de sentimentos
sentiment_lexicon = {
    'positivo': {
        'excelente': 1.0, 'ótimo': 0.9, 'bom': 0.7, 'satisfeito': 0.8, 'feliz': 0.9,
        'contente': 0.8, 'agradável': 0.6, 'maravilhoso': 1.0, 'fantástico': 1.0,
        'incrível': 0.9, 'adorável': 0.8, 'animado': 0.7, 'esperançoso': 0.6,
        'produtivo': 0.7, 'eficiente': 0.7, 'útil': 0.6, 'benéfico': 0.7,
        'promissor': 0.6, 'inovador': 0.7, 'sustentável': 0.6
    },
    'negativo': {
        'péssimo': -1.0, 'terrível': -1.0, 'horrível': -0.9, 'ruim': -0.7, 'insatisfeito': -0.8,
        'triste': -0.8, 'frustrado': -0.9, 'decepcionado': -0.8, 'preocupado': -0.6,
        'difícil': -0.6, 'complicado': -0.6, 'problema': -0.7, 'falha': -0.8,
        'ineficiente': -0.7, 'improdutivo': -0.7, 'prejudicial': -0.8, 'perigoso': -0.9,
        'desafiador': -0.5, 'estressante': -0.7, 'insustentável': -0.6
    }
}

# Palavras de negação
negation_words = {'não', 'nem', 'nunca', 'jamais', 'nada'}

# Intensificadores
intensifiers = {
    'muito': 1.5, 'extremamente': 2.0, 'bastante': 1.3, 'realmente': 1.5,
    'absolutamente': 2.0, 'completamente': 1.8, 'totalmente': 1.8,
    'super': 1.5, 'mega': 1.7, 'ultra': 1.8
}

def lambda_handler(event, context):
    try:
        # Extrair a mensagem do evento
        message = event.get('message')
        
        if not message:
            raise ValueError("Missing 'message' in the event")

        # Analisar o sentimento da mensagem
        sentiment = analyze_sentiment(message)
        
        # Processar a mensagem e gerar uma resposta
        response_content = process_message(message, sentiment)

        # Registrar a informação do processamento
        logger.info(f"Processed message: '{message}' with sentiment: {sentiment}")

        # Retornar o resultado
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': {
                    'content': response_content,
                    'sentiment': sentiment
                }
            })
        }

    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid Input'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }

def process_message(message, sentiment):
    # Aqui você pode adicionar lógica adicional para processar a mensagem
    # Por exemplo, você pode usar NLP para extrair entidades ou intenções
    
    # Por enquanto, vamos apenas gerar uma resposta baseada no sentimento
    base_response = "Entendi sua mensagem."
    return adjust_response_based_on_sentiment(base_response, sentiment)

def preprocess_text(text):
    # Converter para minúsculas
    text = text.lower()
    # Remover pontuação
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenização
    tokens = word_tokenize(text)
    # Remover stop words
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def analyze_sentiment(text):
    tokens = preprocess_text(text)
    sentiment_score = 0
    negation = False
    intensifier = 1

    for token in tokens:
        if token in negation_words:
            negation = True
            continue

        if token in intensifiers:
            intensifier = intensifiers[token]
            continue

        if token in sentiment_lexicon['positivo']:
            score = sentiment_lexicon['positivo'][token] * intensifier
            sentiment_score += -score if negation else score
        elif token in sentiment_lexicon['negativo']:
            score = sentiment_lexicon['negativo'][token] * intensifier
            sentiment_score += -score if negation else score

        negation = False
        intensifier = 1

    if sentiment_score != 0:
        sentiment_score = sentiment_score / abs(sentiment_score) * (1 - 1 / (1 + abs(sentiment_score)))

    if sentiment_score > 0.2:
        return 'positive'
    elif sentiment_score < -0.2:
        return 'negative'
    else:
        return 'neutral'

def adjust_response_based_on_sentiment(content, sentiment):
    if sentiment == 'negative':
        return (f"Percebo que você pode estar enfrentando alguns desafios. "
                f"{content} Estou aqui para ajudar. Há algo específico em que posso focar para melhorar sua situação?")
    elif sentiment == 'positive':
        return (f"Que bom ver você animado! {content} "
                f"Seu entusiasmo é inspirador. Conte-me mais sobre o que está dando certo.")
    else:
        return (f"{content} "
                f"Se houver algo mais em que eu possa ajudar ou esclarecer, por favor, me avise.")