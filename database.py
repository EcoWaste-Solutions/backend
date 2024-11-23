from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


sqlAlchemyDatabaseUrl = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Initialize the database engine
engine = create_engine(sqlAlchemyDatabaseUrl)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DatabaseSessionSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SessionLocal()  # Only create the session once
        return cls._instance


# Modify get_db to use the Singleton instance
def get_db():
    db = DatabaseSessionSingleton.get_instance()
    try:
        yield db
    finally:
        db.close()