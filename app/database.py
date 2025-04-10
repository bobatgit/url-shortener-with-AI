from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    short_code = Column(String, unique=True, index=True)
    original_url = Column(String)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)
    is_custom = Column(Boolean, default=False)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    setting_name = Column(String, unique=True)
    setting_value = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    if settings.environment == "testing":
        # For testing, we want to drop and recreate all tables
        Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Insert default settings if they don't exist
        defaults = [
            ("default_expiry_days", str(settings.default_code_length)),
            ("short_code_length", str(settings.default_code_length)),
            ("allow_custom_urls", "true")
        ]
        for name, value in defaults:
            if not db.query(Setting).filter(Setting.setting_name == name).first():
                db.add(Setting(setting_name=name, setting_value=value))
        db.commit()
    finally:
        db.close()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()