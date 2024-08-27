FROM public.ecr.aws/lambda/python:3.9-x86_64

# Copy requirements.txt and function code
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY moisture_task_planner.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

CMD ["moisture_task_planner.lambda_handler"]