FROM public.ecr.aws/lambda/python:3.8

COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt

CMD ["app.main.lambda_handler"]
