import boto3
import os

s3_client = boto3.client('s3')

def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")

if __name__ == "__main__":
    # Exemplo de uso
    file_path = "path/to/your/file.jpg"
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    s3_key = os.environ.get("S3_KEY")

    upload_to_s3(file_path, bucket_name, s3_key)
