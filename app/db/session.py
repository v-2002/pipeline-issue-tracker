from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

"""
    #the actual connection to database. SQLAlchemy reads DATABASE_URL from config and knows it's SQLite. The connect_args={"check_same_thread": False} is specific to SQLite and allows the connection to be shared across multiple threads, which is necessary for FastAPI's async handling.
    #this is for SQLite, for SQL Server you would not include connect_args
"""
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#SessionLocal is a factory for creating new database sessions. Each time you call SessionLocal(), it will create a new session that is connected to the database defined by the engine. The autocommit=False means that changes to the database won't be automatically committed after each operation, giving you control over when to commit or rollback transactions. The autoflush=False means that changes won't be automatically flushed to the database before queries, which can help prevent unintended side effects during complex operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base is the base class for all your database models. When you define a new model (e.g., User, Issue), you will inherit from Base. This allows SQLAlchemy to keep track of all the models and their corresponding database tables, making it easier to create and manage the database schema.
Base = declarative_base()

#get_db is a dependency function that provides a database session to your API endpoints. 
# When you include get_db as a dependency in your endpoint functions, FastAPI will call this function to create a new database session for each request. 
# The yield statement allows the function to return the session to the endpoint, and once the request is completed, the finally block ensures that the session is properly closed, preventing any potential resource leaks.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()