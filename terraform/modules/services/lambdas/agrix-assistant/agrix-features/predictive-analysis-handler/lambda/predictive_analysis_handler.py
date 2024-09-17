import boto3
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Função handler principal da Lambda de processamento da análise preditiva.
    """
    return predictive_analysis_handler(event, context)

def predictive_analysis_handler(event, context):
    # Carregar ou treinar o modelo
    model = load_or_train_model()
    
    # Fazer previsão com dados atuais
    current_data = pd.DataFrame([event['current_data']])
    prediction = model.predict(current_data)
    
    # Gerar recomendações baseadas na previsão
    recommendations = generate_recommendations(prediction[0])
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'prediction': prediction[0],
            'recommendations': recommendations
        })
    }

def load_or_train_model():
    try:
        # Tentar carregar o modelo existente
        s3.download_file('seu-bucket', 'modelo_rf.joblib', '/tmp/modelo_rf.joblib')
        model = joblib.load('/tmp/modelo_rf.joblib')
        print("Modelo carregado com sucesso.")
    except:
        print("Modelo não encontrado. Treinando novo modelo.")
        model = train_model()
    return model

def train_model():
    # Carregar dados históricos
    obj = s3.get_object(Bucket='seu-bucket', Key='dados_historicos.csv')
    historical_data = pd.read_csv(obj['Body'])
    
    # Preparar os dados e treinar o modelo
    X = historical_data.drop('target', axis=1)
    y = historical_data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avaliar o modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy}")
    
    # Salvar o modelo treinado
    joblib.dump(model, '/tmp/modelo_rf.joblib')
    s3.upload_file('/tmp/modelo_rf.joblib', 'seu-bucket', 'modelo_rf.joblib')
    
    return model

def generate_recommendations(prediction):
    recommendations = {
        'pest_risk': [
            "Considere aplicar pesticidas preventivamente.",
            "Inspecione as plantas regularmente para sinais de pragas.",
            "Implemente métodos de controle biológico, se possível.",
            "Considere o uso de armadilhas para monitoramento de pragas."
        ],
        'disease_risk': [
            "Monitore de perto as plantas para sinais de doenças.",
            "Considere aplicar fungicidas preventivos.",
            "Melhore a circulação de ar entre as plantas.",
            "Evite irrigação excessiva para prevenir condições favoráveis a doenças."
        ],
        'low_yield_risk': [
            "Verifique os níveis de nutrientes do solo e considere a aplicação de fertilizantes.",
            "Otimize as práticas de irrigação.",
            "Considere técnicas de manejo integrado de pragas e doenças.",
            "Avalie a densidade de plantio e ajuste se necessário."
        ],
        'normal': [
            "Continue com as práticas agrícolas normais.",
            "Mantenha o monitoramento regular da plantação.",
            "Considere implementar práticas sustentáveis para melhorar a saúde do solo.",
            "Planeje rotação de culturas para a próxima temporada."
        ]
    }
    
    return recommendations.get(prediction, ["Continue monitorando sua plantação regularmente."])