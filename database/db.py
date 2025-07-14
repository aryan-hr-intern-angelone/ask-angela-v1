from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from config.env import env
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey

db_conn_str = f"postgresql+psycopg2://{env.aws.RDS_USERNAME}:{env.aws.RDS_PASSWORD}@{env.aws.RDS_CONNECTION_URI}:{env.aws.RDS_PORT}/{env.aws.RDS_DATABASE_NAME}"
engine = create_engine(db_conn_str, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    slack_username = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=current_timestamp())
    
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'))
    role = Column(String, nullable=False)
    content = Column(String)
    docs_reffered = Column(String, nullable=True)
    pos_feedback = Column(Boolean, default=False)
    neg_feedback = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=current_timestamp())
    
Base.metadata.create_all(engine)