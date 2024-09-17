import json
import boto3

def advanced_sensor_handler(event, context):
    # Inicializar cliente IoT
    iot = boto3.client('iot-data')

    sensor_data = event['sensor_data']
    
    # Processar e interpretar dados dos sensores
    interpreted_data = interpret_sensor_data(sensor_data)

    # Publicar dados interpretados no tópico IoT
    iot.publish(
        topic='farm/sensors/interpreted',
        payload=json.dumps(interpreted_data)
    )

    return {
        'statusCode': 200,
        'body': json.dumps(interpreted_data)
    }

def interpret_sensor_data(data):
    # Lógica para interpretar dados dos sensores
    return {"soil_composition": {"nitrogen": 0.5, "phosphorus": 0.3, "potassium": 0.2}}