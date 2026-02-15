from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables (e.g., getting DB_URL from .env file)
load_dotenv()

# Example database URL (replace with actual PostgreSQL connection string later)
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") 

# Introduction to SQLAlchemy engine:
# The engine is the starting point for any SQLAlchemy application.
# It handles the connection pool and dialect (SQL format) for your database.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Introduction to SessionLocal:
# Each instance of SessionLocal() will be a database session.
# We create a new session for each request, use it, and then close it.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Introduction to Base:
# The Base class is used to create our database models.
# All models will inherit from this class so SQLAlchemy knows about them.
Base = declarative_base()

# Dependency Injection function for database sessions:
# This function will be used in our API routes to get a database session.
# It ensures the session is closed even if an error occurs.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
