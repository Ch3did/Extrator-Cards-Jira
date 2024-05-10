import os

from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.environ.get("api_token")
EMAIL = os.environ.get("email")
DOMAIN = os.environ.get("domain")

DATABASE_URL = f"sqlite:///tmp/{DOMAIN[8:-10]}.db"
DEBUG = os.environ.get("debug")

# AWS variables
ACCESS_KEY_ID = os.environ.get("access_key_id")
SECRET_ACCESS_KEY = os.environ.get("secret_access_key")
BUCKET = os.environ.get("bucket_name")
