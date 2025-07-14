import boto3
import json
import rich
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

session = boto3.Session()

s3 = session.client('s3')

sqs = session.client(
    service_name='sqs',
    region_name=env.aws.AWS_REGION
)

bucket_name = env.aws.S3_BUCKET_NAME
resource_path = env.aws.S3_BUCKET_RESOURCE_NAME + '/'
queue_url = env.aws.SQS_URL


def get_file(file: S3FileData):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file.resource_name)
        text = response['Body'].read().decode('utf-8')

        chunks, config, tokens = get_text_chunks(text)
        create_vector_store(chunks, file.eTag, file.name, tokens, config)
        create_vector_store_full_docs(text, file.eTag, file.name, tokens)
        
        rich.print(f"[white on blue]S3 Object[/white on blue] File Name: {file.name}, File Size: {file.size} Word Count: {len(text)} words, Approx. Tokens: {len(text)/4}")
    except Exception:
        raise
 
def fetch_existing_resources():
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=resource_path
    )
    
    if 'Contents' in response:        
        for obj in response['Contents']:
            try:
                file = S3FileData(
                    resource_name = obj['Key'],
                    name = obj['Key'].split('/')[1], 
                    eTag = obj['ETag'].strip('"'),
                    size = obj['Size']
                )
                
                if file.name != '':
                    get_file(file)
            except Exception as e:
                rich.print(f"[white on red]Error[/white on red] {str(e)}")
                rich.print("[black on white]Info[/black on white] Skipping current file")
                       
def poll_sqs():
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            

            messages = response.get("Messages", [])
            for msg in messages:
                body_raw= msg.get("Body", {})
                body = json.loads(body_raw)
                record = body.get("Records", [])
                object_data = record[0].get("s3", {}).get("object", {})
                file_name = ul.unquote(ul.unquote_plus(object_data.get("key", "")))
                
                file = S3FileData(
                    resource_name=file_name,
                    name=file_name.split("/")[1],
                    eTag=object_data.get("eTag", ""),
                    size=object_data.get("size", )
                ) 
  
                event_name = record[0].get("eventName", "").split(":")[1]
                
                if event_name == 'Delete':
                    delete_vector_store(file_name.split("/")[1])
                    rich.print(f"[white on grey37]S3 Event[/white on grey37] Deleted - {file_name}") 
                else:
                    get_file(file)
                    rich.print(f"[white on grey37]S3 Event[/white on grey37] Added - {file_name}")  
                    
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg['ReceiptHandle']
                )
        except Exception as e:
            rich.print(f"[white on red]Error[/white on red] {str(e)}")
            rich.print("[black on white]Info[/black on white] Removing Non Event specific messages")
        
def document_listener():
    print("Document Listner Started ...")
    fetch_existing_resources()
    poll_sqs()
