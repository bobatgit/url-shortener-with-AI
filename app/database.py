import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_PATH = Path("data/urls.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True, index=True)
    click_count = Column(Integer, default=0)
    is_custom = Column(Boolean, default=False)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String, unique=True, nullable=False)
    setting_value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    Base.metadata.create_all(bind=engine)
    
    # Insert default settings if they don't exist
    with get_session() as session:
        defaults = [
            ("default_expiry_days", "30"),
            ("short_code_length", "6"),
            ("allow_custom_urls", "true")
        ]
        for name, value in defaults:
            if not session.query(Setting).filter(Setting.setting_name == name).first():
                setting = Setting(setting_name=name, setting_value=value)
                session.add(setting)
        session.commit()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()