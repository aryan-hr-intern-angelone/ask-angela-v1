import os
from dotenv import load_dotenv
from dataclasses import dataclass, field

load_dotenv()

@dataclass
class SlackConfig:
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    SLACK_SOCKET_TOKEN = os.environ.get("SLACK_SOCKET_TOKEN")
    SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
    
@dataclass
class InfrenceProviderConfig:
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    # GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
# @dataclass
# class OAuthConfig:
    # GOOGLE_APLICATION_CREDENTIALS = os.environ.get("GOOGLE_APLICATION_CREDENTIALS")
    # AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    # AZURE_APPLICATION_ID = os.environ.get("AZURE_APPLICATION_ID")
    # AZURE_AUTHORITY_URL = os.environ.get("AZURE_AUTHORITY_URL")
    # CUSTOM_WEBHOOK_URL = os.environ.get("CUSTOM_WEBHOOK_URL")
    
@dataclass
class ModelsConfig:
    EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
    LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
    FLASH_LLM_NAME = os.environ.get("FLASH_LLM_NAME")
    RANKING_MODEL = os.environ.get("RANKING_MODEL")
    
@dataclass
class AWSConfig:
    AWS_PROFILE_NAME = os.environ.get("AWS_PROFILE_NAME")
    RDS_CONNECTION_URI = os.environ.get("RDS_CONNECTION_URI")
    RDS_PORT = os.environ.get("RDS_PORT")
    RDS_USERNAME = os.environ.get("RDS_USERNAME")
    RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
    RDS_DATABASE_NAME = os.environ.get("RDS_DATABASE_NAME")
    DATAMART_HOST = os.environ.get("DATAMART_HOST")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_BUCKET_RESOURCE_NAME = os.environ.get("S3_BUCKET_RESOURCE_NAME")
    AWS_REGION = os.environ.get("AWS_REGION_NAME")
    SQS_URL = os.environ.get("SQS_URL")
    
@dataclass
class DarwinboxConfig:
    DARWINBOX_API_URL = os.environ.get("DARWINBOX_API_URL")
    DARWINBOX_API_KEY = os.environ.get("DARWINBOX_API_KEY")
    DARWINBOX_API_SECRET = os.environ.get("DARWINBOX_API_SECRET") 
    DARWINBOX_API_UID = os.environ.get("DARWINBOX_API_UID")
   
@dataclass
class FAISSConfig:
    INDEX_DIR = os.environ.get("INDEX_DIR") 
    TEXT_CHUNK_PATH = os.environ.get("TEXT_CHUNK_PATH")
    FULL_TEXT_PATH = os.environ.get("FULL_TEXT_PATH")
 
# Primary Data class
@dataclass
class Config:
    slack: SlackConfig = field(default_factory=SlackConfig)
    provider: InfrenceProviderConfig = field(default_factory=InfrenceProviderConfig)
    models: ModelsConfig = field(default_factory=ModelsConfig)
    aws: AWSConfig = field(default_factory=AWSConfig)
    darwinbox: DarwinboxConfig = field(default_factory=DarwinboxConfig)
    faiss: FAISSConfig = field(default=FAISSConfig)

env = Config()