import boto3
from io import BytesIO
import urllib.parse as ul
from config.env import env
from lib.embedding import get_text_chunks, create_vector_store, create_vector_store_full_docs, delete_vector_store
from dataclasses import dataclass

@dataclass
class S3FileData:
    resource_name: str
    name: str
    eTag: str
    size: int

session = boto3.Session(
    profile_name=env.aws.AWS_PROFILE_NAME
)

s3 = session.client('s3')
# sqs = session.client(
#     service_name='sqs',
#     region_name=env.aws.AWS_REGION
# )

bucket_name = env.aws.S3_BUCKET_NAME
resource_path = env.aws.S3_BUCKET_RESOURCE_NAME + '/'
# queue_url = env.aws.SQS_URL

def get_file(file: S3FileData):
    file_obj = BytesIO()
    s3.download_fileobj(bucket_name, file.resource_name, file_obj)
    file_obj.seek(0)
    text = file_obj.read().decode('utf-8')
    
    chunks, config, tokens = get_text_chunks(text)
    create_vector_store(chunks, file.eTag, file.name, tokens, config)
    create_vector_store_full_docs(text, file.eTag, file.name, tokens)
    
    print(f"File Name: {file.name}, File Size: {file.size} Word Count: {len(text)} words, Approx. Tokens: {len(text)/4}") 
    
def fetch_existing_resources():
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=resource_path
    )

    skip = [
        "Employee Referral Policy - Non-Tech.txt",
        "Empolyee_Referral_Product.txt",
        "Copy of Referral Policy Consolidation.txt",
        "Onboarding Guide.txt"
    ]
    
    if 'Contents' in response:        
        for obj in response['Contents']:
            file = S3FileData(
                resource_name = obj['Key'],
                name = obj['Key'].split('/')[1], 
                eTag = obj['ETag'].replace("", ''),
                size = obj['Size']
            )
            
            if file.name != '':
                if file.name in skip:
                    continue
                s3.download_file(bucket_name, file.resource_name, file.name)
                get_file(file)
                       
# def poll_sqs():
#     while True:
#         try:
#             response = sqs.receive_message(
#                 QueueUrl=queue_url,
#                 MaxNumberOfMessages=1,
#                 WaitTimeSeconds=20
#             )
#             messages = response.get("Messages", [])
#             for msg in messages:
#                 body_raw= msg.get("Body", {})
#                 body = json.loads(body_raw)
#                 record = body.get("Records", [])
#                 object_data = record[0].get("s3", {}).get("object", {})
#                 file_name = object_data.get("key", "")
                
#                 resource_id = object_data.get("eTag", "")
#                 file_name = ul.unquote(ul.unquote_plus(file_name))
#                 event_name = record[0].get("eventName", "").split(":")[1]
                
#                 if event_name == 'Deleted':
#                     delete_vector_store(file_name)
#                     print(f"Deleted - {file_name}")
#                 else:
#                     get_file(resource_id, file_name)
#                     print(f"Addedd - {file_name}")
                    
#                 sqs.delete_message(
#                     QueueUrl=queue_url,
#                     ReceiptHandle=msg['ReceiptHandle']
#                 )
#         except Exception as e:
#             raise e
        
def document_listener():
    print("Document Listner Started ...")
    fetch_existing_resources()
    # poll_sqs()
            