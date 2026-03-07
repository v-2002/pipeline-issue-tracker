from pydantic_settings import BaseSettings          #reads values from environment variables and .env file automatically 
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    APP_NAME: str = "Pipeline Issue Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-this-later"
    DATABASE_URL: str = "sqlite:///./pipeline_tracker.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30       #how long the JWT access token should be valid (in minutes) || are for JWT 
    ALGORITHM: str = "HS256"                    #are for JWT token generation and validation, used in authentication processes

    class Config:
        env_file = ".env"  # Specify the .env file to load

settings = Settings()  # Create an instance of the Settings class to access configuration values || settings is a single instance imported everywhere in the app — no need to call os.getenv() scattered across files