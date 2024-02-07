import os

from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.environ.get("api_token")
EMAIL = os.environ.get("email")
DOMAIN = os.environ.get("domain")
DATABASE_URL = os.environ.get("database_url")
DEBUG = os.environ.get("debug")
