import json
import boto3
import os
import logging
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuração dos clientes AWS
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
ses = boto3.client('ses')
cloudwatch = boto3.client('cloudwatch')

# Nome das tabelas e bucket
TASKS_TABLE = os.environ['TASKS_TABLE']
PROFILE_TABLE = os.environ['PROFILE_TABLE']
REPORT_BUCKET = os.environ['REPORT_BUCKET']

def lambda_handler(event, context):
    try:
        report_type = event['report_type']
        if report_type == 'daily':
            return generate_daily_report()
        elif report_type == 'weekly':
            return generate_weekly_report()
        else:
            raise ValueError(f"Invalid report type: {report_type}")
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise

def generate_daily_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    tasks = get_tasks(start_date, end_date)
    metrics = get_metrics(start_date, end_date)
    
    report = format_daily_report(tasks, metrics)
    
    report_key = f"daily_reports/report_{end_date.strftime('%Y-%m-%d')}.html"
    upload_to_s3(report, report_key)
    
    send_email_notification("Relatório Diário Ágrix", report_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Daily report generated successfully')
    }

def generate_weekly_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    tasks = get_tasks(start_date, end_date)
    metrics = get_metrics(start_date, end_date)
    
    report = format_weekly_report(tasks, metrics)
    
    report_key = f"weekly_reports/report_{end_date.strftime('%Y-%m-%d')}.html"
    upload_to_s3(report, report_key)
    
    send_email_notification("Relatório Semanal Ágrix", report_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Weekly report generated successfully')
    }

def get_tasks(start_date, end_date):
    table = dynamodb.Table(TASKS_TABLE)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('timestamp').between(
            start_date.isoformat(),
            end_date.isoformat()
        )
    )
    return response['Items']

def get_metrics(start_date, end_date):
    metrics = {}
    metric_names = ['SoilMoisture', 'SoilTemperature', 'AirMoisture', 'AirTemperature', 'Brightness']
    
    for metric in metric_names:
        response = cloudwatch.get_metric_statistics(
            Namespace='Agrix',
            MetricName=metric,
            StartTime=start_date,
            EndTime=end_date,
            Period=86400,  # 1 day in seconds
            Statistics=['Average', 'Minimum', 'Maximum']
        )
        metrics[metric] = response['Datapoints']
    
    return metrics

def format_daily_report(tasks, metrics):
    completed_tasks = [task for task in tasks if task['status'] == 'completed']
    pending_tasks = [task for task in tasks if task['status'] == 'pending']
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Relatório Diário Ágrix</h1>
        <h2>Tarefas Concluídas: {len(completed_tasks)}</h2>
        <ul>
            {"".join(f"<li>{task['description']}</li>" for task in completed_tasks)}
        </ul>
        <h2>Tarefas Pendentes: {len(pending_tasks)}</h2>
        <ul>
            {"".join(f"<li>{task['description']}</li>" for task in pending_tasks)}
        </ul>
        <h2>Métricas</h2>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Média</th>
                <th>Mínimo</th>
                <th>Máximo</th>
            </tr>
            {"".join(f"<tr><td>{metric}</td><td>{data[0]['Average']:.2f}</td><td>{data[0]['Minimum']:.2f}</td><td>{data[0]['Maximum']:.2f}</td></tr>" for metric, data in metrics.items())}
        </table>
    </body>
    </html>
    """
    return html_content

def format_weekly_report(tasks, metrics):
    completed_tasks = [task for task in tasks if task['status'] == 'completed']
    pending_tasks = [task for task in tasks if task['status'] == 'pending']
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Relatório Semanal Ágrix</h1>
        <h2>Resumo de Tarefas</h2>
        <p>Tarefas Concluídas: {len(completed_tasks)}</p>
        <p>Tarefas Pendentes: {len(pending_tasks)}</p>
        <h2>Progresso Semanal</h2>
        <p>Taxa de Conclusão: {(len(completed_tasks) / (len(completed_tasks) + len(pending_tasks)) * 100):.2f}%</p>
        <h2>Métricas Semanais</h2>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Média</th>
                <th>Mínimo</th>
                <th>Máximo</th>
            </tr>
            {"".join(f"<tr><td>{metric}</td><td>{sum(d['Average'] for d in data) / len(data):.2f}</td><td>{min(d['Minimum'] for d in data):.2f}</td><td>{max(d['Maximum'] for d in data):.2f}</td></tr>" for metric, data in metrics.items())}
        </table>
    </body>
    </html>
    """
    return html_content

def upload_to_s3(report, report_key):
    try:
        s3.put_object(Bucket=REPORT_BUCKET, Key=report_key, Body=report, ContentType='text/html')
    except ClientError as e:
        logger.error(f"Error uploading report to S3: {e}")
        raise

def send_email_notification(subject, report_key):
    SENDER = "agrix@exemplo.com"
    RECIPIENT = "agricultor@exemplo.com"
    
    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
        <h1>{subject}</h1>
        <p>Seu relatório está pronto. Você pode acessá-lo através do seguinte link:</p>
        <p><a href='https://{REPORT_BUCKET}.s3.amazonaws.com/{report_key}'>Ver Relatório</a></p>
    </body>
    </html>
    """
    
    try:
        response = ses.send_email(
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Body': {'Html': {'Charset': "UTF-8", 'Data': BODY_HTML}},
                'Subject': {'Charset': "UTF-8", 'Data': subject},
            },
            Source=SENDER
        )
    except ClientError as e:
        logger.error(f"Error sending email: {e.response['Error']['Message']}")
    else:
        logger.info(f"Email sent! Message ID: {response['MessageId']}")