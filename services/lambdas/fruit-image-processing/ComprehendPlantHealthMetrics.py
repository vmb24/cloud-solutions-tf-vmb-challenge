import json
import boto3

rekognition = boto3.client('rekognition')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PlantHealth')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'POST':
        return create_plant_health_record(json.loads(event['body']))
    elif http_method == 'GET':
        return get_plant_health_record(event['queryStringParameters']['RecordID'])
    elif http_method == 'DELETE':
        return delete_plant_health_record(event['queryStringParameters']['RecordID'])
    else:
        return build_response(405, 'Method Not Allowed')

def create_plant_health_record(data):
    try:
        image = data['Image']
        rekognition_response = analyze_image(image)
        metrics_text = extract_metrics_text(rekognition_response)
        data['RekognitionResult'] = rekognition_response
        data['MetricsText'] = metrics_text
        table.put_item(Item=data)
        return build_response(201, data)
    except Exception as e:
        return build_response(500, str(e))

def get_plant_health_record(record_id):
    try:
        response = table.get_item(Key={'RecordID': record_id})
        if 'Item' in response:
            return build_response(200, response['Item'])
        else:
            return build_response(404, 'Record not found')
    except Exception as e:
        return build_response(500, str(e))

def delete_plant_health_record(record_id):
    try:
        table.delete_item(Key={'RecordID': record_id})
        return build_response(200, 'Record deleted')
    except Exception as e:
        return build_response(500, str(e))

def analyze_image(image):
    try:
        rekognition_response = rekognition.detect_labels(
            Image={'Bytes': image},
            MaxLabels=10,
            MinConfidence=80
        )
        return rekognition_response['Labels']
    except Exception as e:
        return str(e)

def extract_metrics_text(rekognition_response):
    try:
        labels = [label['Name'] for label in rekognition_response]
        text = " ".join(labels)
        comprehend_response = comprehend.detect_entities(Text=text, LanguageCode='pt')
        entities = comprehend_response['Entities']
        return entities
    except Exception as e:
        return str(e)

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
