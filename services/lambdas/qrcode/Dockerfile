# Usando a imagem base Python
FROM public.ecr.aws/lambda/python:3.8

# Instala dependências necessárias
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copia o código da função para o diretório de trabalho
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Define o handler
CMD ["qrcode_lambda_function.lambda_handler"]
