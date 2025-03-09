import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class DatabaseConfig:
    """Encapsulates database configuration and URL construction."""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "db")
        self.port = os.getenv("DB_PORT", "5432")
        self.name = os.getenv("DB_NAME", "testdb")
        self.user = os.getenv("DB_USER", "admin")
        self.password = os.getenv("DB_PASSWORD", "secret")

    def get_database_url(self):
        """Constructs and returns the PostgreSQL connection URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

# Initialize database configuration
db_config = DatabaseConfig()
DATABASE_URL = db_config.get_database_url()

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for ORM models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    """Provides a new database session with error handling."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()  # Rollback changes in case of error
        raise e
    finally:
        db.close()