from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env
load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# PostgreSQL connection details from .env
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")


# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change this in production
ALGORITHM =  os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30) 
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)


# Logger Configuration
logger = logging.getLogger("service_logger")
logger.setLevel(logging.INFO)  # Change to DEBUG for more details

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Avoid duplicate handlers if re-imported
if not logger.handlers:
    logger.addHandler(console_handler)