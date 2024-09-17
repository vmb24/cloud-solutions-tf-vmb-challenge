import json
import boto3
import base64

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento de diagnóstico de imagem.
    """
    return image_diagnosis_handler(event, context)

def image_diagnosis_handler(event, context):
    # Inicializar cliente Rekognition
    rekognition = boto3.client('rekognition')

    # Decodificar a imagem de base64
    image_bytes = base64.b64decode(event['image'])
    
    # Analisar imagem para diagnóstico
    response = rekognition.detect_labels(Image={'Bytes': image_bytes}, MaxLabels=10, MinConfidence=70)

    diagnosis = interpret_labels(response['Labels'])

    return {
        'statusCode': 200,
        'body': json.dumps(diagnosis)
    }

def interpret_labels(labels):
    # Dicionário de mapeamento de labels para diagnósticos
    diagnosis_map = {
        'Yellow Leaf': {'diagnosis': 'Possível deficiência de nitrogênio', 'confidence': 0.0},
        'Brown Spot': {'diagnosis': 'Possível doença fúngica', 'confidence': 0.0},
        'Wilted': {'diagnosis': 'Possível estresse hídrico', 'confidence': 0.0},
        'Insect': {'diagnosis': 'Possível infestação de insetos', 'confidence': 0.0},
    }

    # Inicializar o diagnóstico
    diagnosis = {'diagnosis': 'Planta saudável', 'confidence': 1.0}

    for label in labels:
        label_name = label['Name']
        if label_name in diagnosis_map:
            confidence = label['Confidence'] / 100.0
            if confidence > diagnosis_map[label_name]['confidence']:
                diagnosis_map[label_name]['confidence'] = confidence
                
                # Atualizar o diagnóstico se encontrarmos uma condição com maior confiança
                if confidence > diagnosis['confidence']:
                    diagnosis = diagnosis_map[label_name]
                    diagnosis['confidence'] = confidence

    # Adicionar recomendações baseadas no diagnóstico
    diagnosis['recommendations'] = get_recommendations(diagnosis['diagnosis'])

    return diagnosis

def get_recommendations(diagnosis):
    recommendations = {
        'Possível deficiência de nitrogênio': [
            "Aplique fertilizante rico em nitrogênio",
            "Considere fazer uma análise de solo para confirmar a deficiência",
            "Monitore a irrigação, pois o excesso de água pode lixiviar o nitrogênio"
        ],
        'Possível doença fúngica': [
            "Aplique um fungicida apropriado",
            "Remova e destrua as folhas infectadas",
            "Melhore a circulação de ar ao redor das plantas"
        ],
        'Possível estresse hídrico': [
            "Ajuste o regime de irrigação",
            "Adicione cobertura morta ao solo para reter umidade",
            "Verifique se há problemas de drenagem no solo"
        ],
        'Possível infestação de insetos': [
            "Aplique um inseticida adequado",
            "Introduza predadores naturais, se possível",
            "Inspecione regularmente as plantas para detectar sinais precoces de infestação"
        ],
        'Planta saudável': [
            "Continue com as práticas atuais de cuidado",
            "Monitore regularmente para sinais de mudança na saúde da planta",
            "Considere um programa de fertilização equilibrada para manter a saúde"
        ]
    }
    
    return recommendations.get(diagnosis, ["Consulte um agrônomo para uma avaliação mais detalhada"])