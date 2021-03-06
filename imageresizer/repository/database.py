"""
Database configuration for the sqlite image resizer database
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from imageresizer.settings import settings

SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.cache_dir}/image-resizer.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
