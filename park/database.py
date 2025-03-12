from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

class DBSettings(BaseSettings):
    # Database Configuration
    db_user: str = "root"
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "jakarta_parks"
    
    class Config:
        env_prefix = 'PARKS_DB_'
        env_file = '.env'
        extra = 'ignore'

settings = DBSettings()

DATABASE_URL = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()