from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings 



# sqlAlchemyDatabaseUrl = "postgresql://postgres:iam4yearsold@localhost/wasteManagement"
# sqlAlchemyDatabaseUrl = "postgresql://postgres:iam4yearsold@localhost:5432/wasteManagement"

sqlAlchemyDatabaseUrl = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# sqlAlchemyDatabaseUrl = f"postgresql://{config.Settings.database_username}:{config.Settings.database_password}@{config.Settings.database_hostname}/{config.Settings.database_name}"

engine = create_engine(sqlAlchemyDatabaseUrl)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
