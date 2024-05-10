import os

from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.environ.get("api_token")
EMAIL = os.environ.get("email")
DOMAIN = os.environ.get("domain")

COMPANY_NAME = DOMAIN[8:-10].replace(".atlassian", "")
DATABASE_URL = f"sqlite:///tmp/{COMPANY_NAME}.db"
DEBUG = os.environ.get("debug")

# AWS variables
ACCESS_KEY_ID = os.environ.get("access_key_id")
SECRET_ACCESS_KEY = os.environ.get("secret_access_key")
BUCKET = os.environ.get("bucket_name")
