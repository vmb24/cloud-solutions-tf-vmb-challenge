# syntax=docker/dockerfile:1
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt and function code
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY soil_data_processing_recommendations.py ${LAMBDA_TASK_ROOT}

RUN pip3 install --no-cache-dir -r ./requirements.txt
# Install the specified packages
RUN pip install -r requirements.txt

CMD ["soil_data_processing_recommendations.lambda_handler"]