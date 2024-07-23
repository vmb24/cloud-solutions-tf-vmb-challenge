# Use the official AWS Lambda Python runtime as a parent image
FROM amazon/aws-lambda-python:3.8

# Set the working directory
WORKDIR /var/task

# Copy the requirements file into the container
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the lambda function
CMD ["app.lambda_handler"]
