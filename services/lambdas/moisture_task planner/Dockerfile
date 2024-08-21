FROM public.ecr.aws/lambda/python:3.8

# Copie os arquivos necessários
COPY moisture_task_planner.py requirements.txt ./

# Instale as dependências
RUN pip install -r requirements.txt

COPY moisture_task_planner.py ${LAMBDA_TASK_ROOT}

CMD ["moisture_task_planner.lambda_handler"]