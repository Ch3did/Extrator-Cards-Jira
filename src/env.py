import os

from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.environ.get("api_token")
EMAIL = os.environ.get("email")
DOMAIN = os.environ.get("domain")

COMPANY_NAME = DOMAIN[8:-10].replace(".atlassian", "")
DATABASE_URL = f"sqlite:///tmp/{COMPANY_NAME}.db"
DEBUG = os.environ.get("debug")

# Elasticsearch
ELASTIC_HOST = os.environ.get("elastic_host", "localhost")
ELASTIC_PORT = int(os.environ.get("elastic_port", 9200))
