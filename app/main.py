from fastapi import FastAPI
from dotenv import load_dotenv      #reads your .env file and loads everything into environment variables
import os                           #reads the environment variables set in .env file

load_dotenv()                       #loads the .env file and makes the variables available in os.environ

app = FastAPI(
    title=os.getenv("APP_NAME", "Pipeline Issue Tracker"),
    description="Track and manage data pipeline failures and issues",
    version=os.getenv("APP_VERSION", "1.0.0"),                          #os.getenv() reads the value of the environment variable, .env file  is read
    redoc_url="/redoc"                                                  #docs_url="/docs" tells FastAPI where to serve the auto-generated documentation.
)

@app.get("/")                        #Defines a GET endpoint at the root level. whnever someone send a GET req, this function (read_root) will be executed and return a welcome message as a JSON response.   
def read_root():
    return {"Hello": "Welcome to the Pipeline Issue Tracker API!"}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": os.getenv("APP_NAME"),
        "version": os.getenv("APP_VERSION")
    }

