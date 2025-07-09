import enum
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Enum, ForeignKey

engine = create_engine('sqlite:///database.db', echo=True)

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
    
# class Files(Base):
#     __tablename__ = "files"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     file_name = Column(String, nullable=False)
#     size = Column(String, nullable=False)
#     added_on = Column(DateTime, default=datetime.now())
#     updated_on = Column(DateTime)

Base.metadata.create_all(engine)