from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
import os

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    short_code = Column(String, unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    click_count = Column(Integer, default=0)
    is_custom = Column(Boolean, default=False)
    
    __table_args__ = (
        Index('idx_short_code', 'short_code'),
        Index('idx_expires_at', 'expires_at'),
    )

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_name = Column(String, unique=True, nullable=False)
    setting_value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

DATABASE_URL = os.getenv('DATABASE_PATH')
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        if not session.query(Settings).count():
            default_settings = [
                Settings(setting_name='default_expiry_days', setting_value='30'),
                Settings(setting_name='short_code_length', setting_value='6'),
                Settings(setting_name='allow_custom_urls', setting_value='true')
            ]
            session.add_all(default_settings)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session