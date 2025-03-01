from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DBSettings(BaseSettings):
    # Database Configuration
    db_user: str
    db_password: str
    db_host: str
    db_port: int 
    db_name: str
    
    # Auth Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    google_client_id: str
    
    class Config:
        env_prefix = 'AUTH_DB_'
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