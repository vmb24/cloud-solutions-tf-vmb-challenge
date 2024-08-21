FROM public.ecr.aws/lambda/python:3.8

# Copie os arquivos necessários
COPY soil_data_processing_recommendations.py requirements.txt ./

# Instale as dependências
RUN pip install -r requirements.txt

COPY soil_data_processing_recommendations.py ${LAMBDA_TASK_ROOT}

CMD ["soil_data_processing_recommendations.lambda_handler"]