import os
import boto3
from io import BytesIO
from config.env import env
from utils.embedding import get_text_chunks, create_vector_store, create_vector_store_full_docs

session = boto3.Session(
    profile_name=env.aws.AWS_PROFILE_NAME
)

s3 = session.client('s3')

bucket_name = env.aws.S3_BUCKET_NAME
resource_path = env.aws.S3_BUCKET_RESOURCE_NAME + '/'

response = s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix=resource_path
)

skip = [
    "Employee Referral Policy - Non-Tech.txt",
    "Empolyee_Referral_Product.txt",
    "Pitch a Friend Policy Data.txt",
    "Pitch a Friend Policy.txt",
    "Copy of Referral Policy Consolidation.txt",
]

def fetch_resources():
    if 'Contents' in response:        
        for obj in response['Contents']:
            file_name = obj['Key'].split('/')[1]
            
            if file_name != '':
                if file_name in skip:
                    continue
                
                file_obj = BytesIO()
                s3.download_fileobj(bucket_name, obj['Key'], file_obj)
                file_obj.seek(0)
                data_text = file_obj.read().decode('utf-8')
                
                chunks = get_text_chunks(data_text)
                create_vector_store(chunks, obj["ETag"], file_name)
                create_vector_store_full_docs(data_text, obj["ETag"], file_name)
                
                print(f"File Name: {file_name}, Size: {len(data_text)} words, Approx. Tokens: {len(data_text)/4}") 
        
            